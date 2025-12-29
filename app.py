import gradio as gr
from openai import OpenAI
import re
import random
import json
import os
from datetime import datetime

# client 設定
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL_NAME = "gemma2:27b"

# --- 風格與導演設定 ---
STYLES = {
    "標準敘事": "平衡對話與描寫，推動劇情為主。",
    "沉浸感官": "著重描寫視覺、聽覺、觸覺、氣味與角色的生理反應，節奏較慢。",
    "心理獨白": "深入角色的內心糾結、慾望與矛盾，強調心理活動。",
    "激烈動作": "使用短句，強調速度感、衝擊力與暴力美學，減少心理描寫。",
    "暗黑壓抑": "強調環境的陰暗、絕望感與恐怖氛圍，用詞晦澀。",
    "意識流": "打破邏輯邊界，夢幻、錯亂、跳躍的思考。",
}

DIRECTOR_CUTS = [
    "【特寫鏡頭】忽略周遭，極度專注於描寫角色臉部微表情與肢體細節。",
    "【環境敘事】在動作發生前，先花 50 字描寫周遭的聲音、光影或天氣。",
    "【非線性敘事】插入一段極短的回憶或幻覺，打斷當前動作。",
    "【極簡主義】減少形容詞，用動詞主導畫面，快節奏。",
    "【感官過載】強調「氣味」與「觸覺」的黏膩感。",
    "【內心解離】描寫角色雖然在做某事，但思緒飄到了別處。",
    "【直接切入】無過場，第一句話就是動作或對話。",
    "【沈默張力】減少對話，強調沈默中的尷尬或張力。",
    None, None, None, None
]

# --- 核心邏輯函數 ---

def add_empty_row(current_data, col_count):
    """手動新增一行空白資料"""
    if current_data is None:
        return [["" for _ in range(col_count)]]
    return current_data + [["" for _ in range(col_count)]]

def get_lore_injection(lore_data, current_context):
    injected_lore = []
    if lore_data:
        for row in lore_data:
            if row[0]:
                keyword = str(row[0]).strip()
                desc = str(row[1]).strip() if len(row) > 1 else ""
                if keyword and keyword in current_context:
                    injected_lore.append(f"【詞條：{keyword}】{desc}")
    
    if injected_lore:
        return "\n[觸發世界觀補充]\n" + "\n".join(injected_lore)
    return ""

def generate_prompt(background, roles_data, lore_data, current_story, instruction, style_key):
    # 1. 角色
    char_desc_list = []
    if roles_data:
        for row in roles_data:
            if row[0] and str(row[0]).strip():
                role_bg = row[1] if len(row) > 1 else ""
                role_pers = row[2] if len(row) > 2 else ""
                char_desc_list.append(f"- {row[0]}: 背景<{role_bg}>; 性格<{role_pers}>")
    char_desc = "\n".join(char_desc_list) or "（無）"

    # 2. 截取上下文
    recent_story = current_story[-3500:] if len(current_story) > 3500 else current_story
    
    # 3. 觸發 Lorebook
    lore_text = get_lore_injection(lore_data, recent_story + instruction)

    # 4. 風格與導演
    style_guide = STYLES.get(style_key, STYLES["標準敘事"])
    hidden_directive = random.choice(DIRECTOR_CUTS)
    hidden_text = f"\n★ 隱藏挑戰：{hidden_directive}" if hidden_directive else ""

    prompt = f"""
你是一位殿堂級小說家，擅長 {style_key} 風格。
請嚴格遵守以下規則續寫。

【世界觀背景】
{background}

【登場角色】
{char_desc}

【動態世界觀補充 (Lorebook)】
{lore_text}

【風格要求：{style_key}】
{style_guide}
{hidden_text}

【寫作禁忌】
1. 嚴禁結尾總結或說教。
2. 拒絕重複形容詞，多用感官描寫 (Show, Don't Tell)。
3. 禁止替使用者決定後續長遠發展，只寫當下。

【目前劇情】
...
{recent_story}

【本段指令】
{instruction}

【思考 (Chain of Thought)】
請先在 <think> 標籤中規劃：
1. 核心衝突點。
2. 檢查是否觸發了 Lorebook 中的設定，若有請確保描述一致。
3. 規劃一個獨特的感官細節。

【正文輸出】
"""
    return prompt

# 修改：新增 max_len 參數
def generate_continuation(background, roles_data, lore_data, current_story, instruction, style, temp, freq_penalty, max_len):
    if not instruction.strip():
        return current_story, current_story, "請輸入指令！", ""

    prompt = generate_prompt(background, roles_data, lore_data, current_story, instruction, style)
    
    history_state = current_story

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            frequency_penalty=freq_penalty,
            presence_penalty=0.4,
            max_tokens=int(max_len), # 這裡使用滑桿傳進來的數值
            top_p=0.9,
        )
        raw_content = response.choices[0].message.content.strip()
        
        think_match = re.search(r'<think>(.*?)</think>', raw_content, re.DOTALL)
        if think_match:
            thought_process = think_match.group(1).strip()
            new_part = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
        else:
            thought_process = "（無思考過程）"
            new_part = raw_content

    except Exception as e:
        new_part = f"（生成錯誤：{str(e)}）"
        thought_process = "Error"
    
    updated_story = current_story + "\n\n" + new_part
    
    return updated_story, history_state, new_part, thought_process

# --- 存檔/讀檔/Undo 功能 ---

def save_project(bg, roles, lore, story):
    roles_list = roles.values.tolist() if hasattr(roles, 'values') else roles
    lore_list = lore.values.tolist() if hasattr(lore, 'values') else lore

    data = {
        "background": bg,
        "roles": roles_list,
        "lore": lore_list,
        "story": story,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    filename = f"story_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def load_project(file_obj):
    if file_obj is None:
        return [gr.update()]*4
    
    try:
        with open(file_obj.name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return (
            data.get("background", ""),
            data.get("roles", []),
            data.get("lore", []),
            data.get("story", "")
        )
    except Exception as e:
        print(f"Load Error: {e}")
        return [gr.update()]*4

def undo_last_step(history_story):
    if not history_story:
        return "（沒有上一步紀錄）", "（無）"
    return history_story, "已還原到上一步！"

# --- 介面設計 ---
with gr.Blocks() as demo:
    
    state_history = gr.State("")

    gr.Markdown("# 🌑 AI 深度寫作助手 v2.2 (長度控制版)")
    
    with gr.Tab("1. 世界與角色設定"):
        with gr.Row():
            with gr.Column(scale=1):
                background_input = gr.Textbox(label="🌍 故事背景 (World)", lines=10, placeholder="輸入世界觀、主要場景...")
            with gr.Column(scale=1):
                gr.Markdown("### 💾 專案管理")
                save_btn = gr.Button("下載存檔 (.json)", variant="secondary")
                save_file = gr.File(label="下載連結", interactive=False)
                
                gr.Markdown("---")
                load_btn = gr.UploadButton("📂 讀取存檔", file_types=[".json"], variant="secondary")
                load_msg = gr.Markdown("")

        with gr.Accordion("👥 角色設定 (Characters)", open=True):
            gr.Markdown("請在下方輸入角色。若要增加角色，請點擊「➕ 新增一列」按鈕。")
            roles_input = gr.Dataframe(
                headers=["名稱", "背景簡述", "性格與語氣"],
                column_count=(3, "fixed"),
                row_count=(1, "dynamic"),
                type="array",
                interactive=True,
                wrap=True,
                label="角色列表"
            )
            add_role_btn = gr.Button("➕ 新增角色欄位", size="sm", variant="secondary")

        with gr.Accordion("📖 世界觀詞條 (Lorebook)", open=False):
            gr.Markdown("設定專有名詞，AI 提到關鍵字時才會讀取。")
            lore_input = gr.Dataframe(
                headers=["關鍵字", "詳細設定"],
                column_count=(2, "fixed"),
                row_count=(1, "dynamic"),
                type="array",
                interactive=True,
                wrap=True,
                label="詞條列表"
            )
            add_lore_btn = gr.Button("➕ 新增詞條欄位", size="sm", variant="secondary")
        
        start_btn = gr.Button("設定完成，開始創作 →", variant="primary")

    with gr.Tab("2. 互動創作"):
        with gr.Column(visible=False) as writing_area:
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("### 📝 故事畫布")
                    full_story_box = gr.Textbox(label="全文 (可直接編輯)", lines=25, interactive=True)
                    
                    with gr.Row():
                        undo_btn = gr.Button("↩️ 復原 (Undo)", size="sm", variant="secondary")
                        clear_btn = gr.Button("🗑️ 清空", size="sm", variant="stop")

                with gr.Column(scale=1):
                    gr.Markdown("### 🎬 導演控制台")
                    style_dropdown = gr.Dropdown(list(STYLES.keys()), value="標準敘事", label="風格")
                    
                    with gr.Group():
                        temp_slider = gr.Slider(0.1, 1.5, value=0.9, step=0.1, label="創意度 (Temp)")
                        freq_slider = gr.Slider(0.0, 2.0, value=0.6, step=0.1, label="重複懲罰 (Penalty)")
                        
                        # 新增：長度滑桿
                        len_slider = gr.Slider(200, 3000, value=1200, step=100, label="生成長度 (Length)", info="Max Tokens: 決定這次續寫的字數上限")

                    instruction = gr.Textbox(label="導演指令", lines=5, placeholder="接下來發生什麼？")
                    generate_btn = gr.Button("✨ 生成續寫", variant="primary")
                    
                    with gr.Accordion("🧠 AI 思考過程 (CoT)", open=False):
                        thought_output = gr.Markdown("...")
                    
                    latest_output = gr.Markdown("...")

    # --- 事件綁定 ---
    
    add_role_btn.click(lambda d: add_empty_row(d, 3), inputs=roles_input, outputs=roles_input)
    add_lore_btn.click(lambda d: add_empty_row(d, 2), inputs=lore_input, outputs=lore_input)

    start_btn.click(
        lambda: (gr.update(visible=True), gr.update(visible=False)),
        outputs=[writing_area, save_file]
    )

    # 記得把 len_slider 加進 inputs 列表
    generate_btn.click(
        generate_continuation,
        inputs=[background_input, roles_input, lore_input, full_story_box, instruction, style_dropdown, temp_slider, freq_slider, len_slider],
        outputs=[full_story_box, state_history, latest_output, thought_output]
    )

    save_btn.click(
        save_project,
        inputs=[background_input, roles_input, lore_input, full_story_box],
        outputs=save_file
    )

    load_btn.upload(
        load_project,
        inputs=load_btn,
        outputs=[background_input, roles_input, lore_input, full_story_box]
    ).then(
        lambda: "存檔讀取成功！", outputs=load_msg
    )

    undo_btn.click(
        undo_last_step,
        inputs=state_history,
        outputs=[full_story_box, latest_output]
    )
    
    clear_btn.click(lambda: "", outputs=full_story_box)

demo.launch(server_port=7860, share=False)