import asyncio
import shutil
import zipfile
import datetime
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import ctypes
import os

BOT_TOKEN = "telegram_bot_token"
DATA_FOLDER = "datas"

STATE_CHOOSE_DISK, STATE_CHOOSE_FOLDERS, STATE_CONFIRM_BACKUP = range(3)

def get_removable_disks():
    kernel32 = ctypes.windll.kernel32
    disk_list = []
    for letter in range(65, 91):
        path = f"{chr(letter)}:\\"
        if kernel32.GetDriveTypeW(path) == 2:
            disk_list.append(path)
    return disk_list

def size_to_human(num_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0:
            return f"{size:3.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}PB"

async def cmd_start(update, context):
    disks = get_removable_disks()
    if not disks:
        await update.message.reply_text("No removable disks detected.")
        return ConversationHandler.END
    
    keyboard = [[d] for d in disks]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Please choose disk:", reply_markup=markup)
    return STATE_CHOOSE_DISK

async def handle_disk_choice(update, context):
    disk_chosen = update.message.text
    path_disk = Path(disk_chosen)
    context.user_data['disk_path'] = path_disk

    folder_names = [f.name for f in path_disk.iterdir() if f.is_dir() and f.name != DATA_FOLDER]
    if not folder_names:
        await update.message.reply_text("No folders on this disk.")
        return ConversationHandler.END

    await update.message.reply_text("Folders found:\n" + "\n".join(folder_names))
    await update.message.reply_text(
        "Write folder names separated by comma, or type 'all' to copy all.",
        reply_markup=ReplyKeyboardRemove()
    )
    return STATE_CHOOSE_FOLDERS

async def handle_folder_choice(update, context):
    user_text = update.message.text.strip().lower()
    disk_path = context.user_data['disk_path']

    if user_text == 'all':
        chosen = [f.name for f in disk_path.iterdir() if f.is_dir() and f.name != DATA_FOLDER]
    else:
        chosen = [x.strip() for x in user_text.split(',')]

    valid = [name for name in chosen if (disk_path / name).exists()]
    if not valid:
        await update.message.reply_text("No such folder(s). Try again or /cancel")
        return ConversationHandler.END

    context.user_data['folders_chosen'] = valid
    keyboard = [["Yes", "No"]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        f"Selected folders: {', '.join(valid)}\nContinue backup?",
        reply_markup=markup
    )
    return STATE_CONFIRM_BACKUP

async def handle_backup(update, context):
    answer = update.message.text.lower()
    if answer != "yes":
        await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    disk_path = context.user_data['disk_path']
    folder_names = context.user_data['folders_chosen']
    backup_root = disk_path / DATA_FOLDER
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = backup_root / f"Dump_{timestamp}"
    backup_folder.mkdir(parents=True, exist_ok=True)

    await update.message.reply_text("Copying folders, wait...")

    def copy_one(name):
        src = disk_path / name
        dst = backup_folder / name
        shutil.copytree(src, dst)
        total_size = sum(f.stat().st_size for f in dst.rglob('*') if f.is_file())
        return total_size

    tasks = [asyncio.to_thread(copy_one, n) for n in folder_names]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    total_bytes = sum(r for r in results if isinstance(r, (int, float)))

    zip_path = backup_root / f"{backup_folder.name}.zip"
    await asyncio.to_thread(
        shutil.make_archive,
        str(zip_path.with_suffix('')),
        'zip',
        backup_folder
    )

    zip_size = zip_path.stat().st_size
    readable = size_to_human(zip_size)

    await update.message.reply_text(f"Backup ready. Size: {readable}", reply_markup=ReplyKeyboardRemove())

    if zip_size < 50 * 1024 * 1024:
        with open(zip_path, "rb") as f:
            await update.message.reply_document(f)
    else:
        await update.message.reply_text("File too big to send (50MB limit).")

    return ConversationHandler.END

async def cmd_cancel(update, context):
    await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            STATE_CHOOSE_DISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_disk_choice)],
            STATE_CHOOSE_FOLDERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_folder_choice)],
            STATE_CONFIRM_BACKUP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_backup)],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    )

    app.add_handler(conv)
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
