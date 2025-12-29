# 📝 AI Deep Writing Assistant v2.2 - Installation & Usage Guide

Hello! This is a local AI writing tool that uses your graphics card for computation. Since it is self-hosted, it is completely free, private, and secure. Please follow the steps below to install:

---

## ⚠️ Recommended Specifications

* **OS**: Windows 10 or 11
* **GPU**: NVIDIA GPU recommended (8GB+ VRAM for a better experience).
* **Disk**: Please reserve about 20GB of space (for downloading AI models).

---

## Step 1: Environment Setup (One-time only)

### 1. Install Python
* Download from the official website: [Python 3.10 Download Link](https://www.python.org/downloads/)
* **Important:** During installation, make sure to check **"Add Python to PATH"** at the bottom, otherwise the program will not run.

### 2. Install AI Engine (Ollama)
* Download and install from the official website: [Ollama Official Site](https://ollama.com/)
* After installation, confirm that a small "Alpaca" icon appears in the system tray (bottom right corner of your screen).

### 3. Download AI Model
* Press `Win + R` on your keyboard, type `cmd`, and press Enter to open the terminal.
* Copy and paste the following command and press Enter (Download is about 15GB, please be patient):
```bash
ollama run gemma2:27b
```
*(Note: If your GPU memory is less than 10GB and it feels slow, please use `ollama run gemma2:9b` instead)*
* When the dialogue cursor appears, it means success. You can close the window.

---

## Step 2: Configure Writing Assistant (One-time only)

1. Extract the compressed package to your desktop or preferred location.
2. Enter the extracted folder.
3. Click on the **address bar** at the top of the folder window, type `cmd`, and press Enter.
4. In the black terminal window, type the following command to install the necessary packages:
```bash
pip install -r requirements.txt
```
5. Wait for it to finish. Once you see `Successfully installed...`, you can close the window.

---

## Step 3: Start Writing

1. Double-click **`啟動.bat`** in the folder.
2. A black terminal window will pop up, **please do not close it**.
3. Your browser will automatically open the writing interface (if not, manually enter `http://127.0.0.1:7860`).
4. Enjoy your creation!

---

## ❓ FAQ

* **Q: Cannot open, showing "Connection refused"?**
  * A: Please make sure Ollama (the Alpaca icon) is running in the system tray.

* **Q: The terminal window flashes and closes immediately?**
  * A: Usually, it's because Python is not installed correctly or the package installation command in Step 2 was not executed.

* **Q: Generation speed is very slow?**
  * A: This runs locally and depends on your GPU performance. You can adjust the "Response Length" to be shorter in the right panel or use a smaller model (`gemma2:9b`).
