# 📝 AI Deep Writing Assistant v3.0 - Installation & Usage Guide

Hello! This is a local AI writing tool that uses your graphics card for computation. Since it is self-hosted, it is completely free, private, and secure. Version 3.0 adds Plot Memory, Language Selection, and Model Quick-Select.

---

## ⚠️ Recommended Specifications

* **OS**: Windows 10 or 11
* **GPU**: NVIDIA GPU recommended
    * **Elite Experience**: 16GB+ VRAM (can run `gemma2:27b` or `command-r`)
    * **Smooth Experience**: 8GB - 12GB VRAM (can run `gemma2:9b` or `mistral-nemo`)
* **Disk**: Please reserve about 20GB - 40GB space (for storing AI models).

---

## Step 1: Environment Setup (One-time only)

### 1. Install Python
* [Download Link (Python 3.10)](https://www.python.org/downloads/)
* **Important:** Make sure to check **"Add Python to PATH"** during installation.

### 2. Install AI Engine (Ollama)
* [Ollama Official Site](https://ollama.com/)
* After installation, confirm that the "Alpaca" icon appears in your system tray.

### 3. Project Configuration
1. Extract the project folder.
2. Type `cmd` in the folder's address bar and press Enter.
3. Run the following command to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 2: How to Change/Download New Models (From Scratch)

If you want to try different AI "personalities," follow these steps:

### 1. Pick a Model
Visit the [Ollama Model Library](https://ollama.com/library) to see all available options. Recommendations:
* `gemma2:27b`: High logic and detailed writing (requires high VRAM).
* `command-r`: Designed for long-form text and roleplay; very few moral lectures.
* `mistral-nemo`: Great balance, suitable for 12GB VRAM cards.

### 2. Download the Model
1. Press `Win + R`, type `cmd`, and press Enter.
2. Type `ollama run <model_name>`. For example, to get `command-r`:
   ```bash
   ollama run command-r
   ```
3. Wait for the download to complete. When the chat prompt appears, the model is installed.
4. **Just close the window**; the model handles everything in the background.

---

## Step 3: Start Writing

1. Double-click **`啟動.bat`**.
2. Once the browser opens, in the **"⚙️ Core Settings"** tab:
   - **Model Quick-Select**: Select your downloaded model from the dropdown (or type the name manually).
   - **Story Memory**: For long stories, input a summary of key events here. The AI will never forget these details.
3. Click **"Setup Finished, Start Writing →"**.

---

## 🌟 v3.0 Feature Highlights

* **🧠 Story Memory**: A dedicated context area that stays in the AI's mind regardless of story length.
* **🖋️ Style DNA Mimicry**: **[New]** Upload your past works, and the AI will analyze your specific writing style and tone to perfectly mimic your personal touch.
* **🌍 Multi-language**: Supports output in Traditional Chinese, Simplified Chinese, English, Japanese, and Korean.
* **🖋️ Format Control**: Customize "Dialogue Ratio" and "Paragraph Density."
* **👁️ Sensory Weights**: Adjust percentages for Visual, Auditory, Tactile, and other sensory descriptions.

---

## ❓ FAQ

* **Q: No response after clicking generate?**
  * A: Check the black terminal window for errors and ensure Ollama (alpaca icon) is running.
* **Q: It's very slow after changing models?**
  * A: If the model is too large (e.g., a 27b model) for your GPU's VRAM, the system will switch to CPU, which is much slower. Try a smaller model (e.g., the 9b series).
