import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# JANGAN GANTI TULISAN DI BAWAH INI DENGAN NOMOR TOKEN!
# Biarkan tetap 'BOT_TOKEN'. Kita akan isi token aslinya di Railway.
TOKEN = os.getenv('BOT_TOKEN')

def scrape_kbbi(kata):
    url = f"https://kbbi.kemendikdasmen.go.id/entri/{kata}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        daftar_arti = soup.find_all('li')
        
        if not daftar_arti:
            return "Maaf, kata tersebut tidak ditemukan."

        hasil = []
        for i, arti in enumerate(daftar_arti, 1):
            teks_arti = arti.get_text().strip()
            if teks_arti and len(teks_arti) > 5:
                hasil.append(f"{i}. {teks_arti}")
        
        return "\n\n".join(hasil[:5]) if hasil else "Kata tidak ditemukan."
    except:
        return "Terjadi gangguan koneksi ke server KBBI."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirimkan satu kata untuk mencari artinya di KBBI.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kata = update.message.text
    await update.message.reply_text(f"Mencari arti kata: **{kata}**...", parse_mode='Markdown')
    definisi = scrape_kbbi(kata)
    await update.message.reply_text(f"**{kata}**:\n\n{definisi}", parse_mode='Markdown')

if __name__ == '__main__':
    # Jika TOKEN kosong, bot akan memberikan pesan error di Logs
    if not TOKEN:
        print("ERROR: BOT_TOKEN tidak ditemukan di Variables Railway!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("Bot KBBI Resmi Berjalan...")
        app.run_polling()
