from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import pandas as pd
import os

students = pd.read_csv("students.csv")

TOKEN = '8154508453:AAFxF4ja1EY5H3neOrwrUw5-mLVa91ALMRA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ваш ID или ФИО, чтобы получить сертификат.")

async def get_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    result = students[students['id'].astype(str) == query]
    if result.empty:
        result = students[students['full_name'].str.lower() == query]

    if not result.empty:
        cert_path = result.iloc[0]['certificate']
        if os.path.exists(cert_path):
            await update.message.reply_document(document=open(cert_path, 'rb'))
        else:
            await update.message.reply_text("Файл сертификата не найден.")
    else:
        await update.message.reply_text("Сертификат не найден. Проверьте ID или ФИО.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_certificate))
    print("Бот запущен...")
    app.run_polling()
