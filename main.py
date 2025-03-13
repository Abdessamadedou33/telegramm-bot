from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re, os
from keep_alive import keep_alive

keep_alive()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("أرسل لي ملفًا وسأقوم بتصفية النتائج وإعادتها لك في ملف.")

async def filter_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.document:
        await update.message.reply_text("الرجاء إرسال ملف نصي.")
        return

    file_id = update.message.document.file_id
    original_filename = update.message.document.file_name
    new_file = await context.bot.get_file(file_id)
    file_path = "input.txt"
    await new_file.download_to_drive(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    filtered_lines = []
    for line in lines:
        if re.search(r".*[dD][aA][tT][aA].*|.*[jJ][oO][iI][nN].*|.*1 8 7.*", line):
            continue
        if re.search(r".*[uU][lL][uU].*|.*[kK].*[eE].*[nN].*|.*FULL MAIL ACCESS.*|.*VALID.*|.*JOIN PRIVATE CLOUD TELEGRAM CHANNEL.*|.*https://t.me/.*|.*DAILY UPDATE WITH NEW FILES.*|.*EU / USA / CORPS / MIXED.*|^=+$|.*(7.*){2,}7.*|.*([hH].*[uU].*){2,}.*|.*[tT][gG].*|.*[cC][oO][mM][bB][oO][sS][oO][uU][rR][cC][eE][sS].*|.*[hH].*[uU].*[lL].*[uU].*", line):
            continue
        if line.strip():  # Only append non-empty lines
            filtered_lines.append(line)

    if filtered_lines:
        # Determine output filename based on original filename
        if re.search(r'[hH][oO][tT][mM][aA][iI][lL]', original_filename):
            result_filename = "Hotmail fresh.txt"
        elif re.search(r'[mM][iI][xX]', original_filename):
            result_filename = "Mix fresh.txt"
        else:
            result_filename = "fresh_results.txt"

        result_path = "output.txt"
        with open(result_path, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)

        await update.message.reply_document(document=result_path, filename=result_filename)
        os.remove(file_path)
        os.remove(result_path)
    else:
        await update.message.reply_text("لم يتم العثور على أي بيانات صالحة بعد التصفية.")

def main():
    TOKEN = "7718866881:AAFbuneZP9a5zVCxTOnVfrqRcLFYM9u-5ts"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, filter_file))

    app.run_polling()

if __name__ == "__main__":
    main()
