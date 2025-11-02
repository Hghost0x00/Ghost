# 👻 GhostDump

> A Telegram bot that silently backs up your USB drive folders and vanishes without a trace.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**GhostDump** is your invisible backup assistant that detects USB drives, creates timestamped archives, and delivers them straight to your Telegram. Like a ghost, it works quietly in the background—but leaves solid proof it was there. 👻💾

---

## 📋 Requirements

- 🐍 Python 3.7 or higher
- 💻 Windows OS (uses Windows API for drive detection)
- 📦 Python packages:
  ```
  python-telegram-bot
  ```

---

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Hghost0x00/GhostDump.git
cd GhostDump
```

### 2️⃣ Install Dependencies
```bash
pip install python-telegram-bot
```

### 3️⃣ Get Your Telegram Bot Token
1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the prompts
3. Choose a name (e.g., "GhostDump Bot")
4. Copy the token you receive

### 4️⃣ Configure Your Bot
Update the `BOT_TOKEN` variable in the code:
```python
BOT_TOKEN = "telegram_bot_token"
```
---

## 🎮 Usage

### Starting the Bot

```bash
python ghostdump.py
```

You should see:
```
Bot is running...
```

### Using GhostDump

1. 💬 **Open Telegram** and find your bot
2. 📤 **Send** `/start` to begin
3. 🎯 **Follow the prompts:**

```
👻 Step 1: Select a Drive
┗━ Choose from detected USB drives (e.g., E:\)

📁 Step 2: Choose Folders
┗━ Type folder names separated by commas
┗━ Or type 'all' to backup everything

✅ Step 3: Confirm
┗━ Type "Yes" to proceed or "No" to cancel
```

4. ⏳ **Wait** for the magic to happen:
   - ✅ Folders copied to `datas/Dump_TIMESTAMP/`
   - 🗜️ ZIP archive created
   - 📊 Size displayed
   - 📱 File sent to Telegram

---

## ⚠️ Important Notes

### 💻 Windows Only
GhostDump uses Windows-specific APIs (`ctypes.windll.kernel32`) to detect removable drives. It won't work on Linux or macOS without modifications.

---

## 📝 License

This project is provided as-is for personal use. Feel free to modify and distribute!

---

## 👤 Author

**Hghost010**

Credit : [1hehaq](https://github.com/1hehaq), [coffinxp](https://github.com/coffinxp), [AnonKryptiQuz](https://github.com/AnonKryptiQuz), [Naho666](https://github.com/Naho666), [Nuknov](https://github.com/Nuknov)

---

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

<div align="center">

**Made with 👻 by Hghost010**

*Backup like a ghost, restore like a pro.*

</div>
