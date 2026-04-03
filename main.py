import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Ambil token dari Railway/Koyeb (Environment Variable)
TOKEN = os.getenv('8396571741:AAGwjMUqTIqIqSkw3HmMSSE0SLSrMVrbkq4')

def scrape_kbbi(kata):
    # URL resmi KBBI
    url = f"https://kbbi.kemendikdasmen.go.id/entri/{kata}"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari elemen arti kata dalam tag <li>
        daftar_arti = soup.find_all('li')
        
        if not daftar_arti:
            return "Maaf, kata tersebut tidak ditemukan."

        hasil = []
        for i, arti in enumerate(daftar_arti, 1):
            teks_arti = arti.get_text().strip()
            # Filter agar hanya mengambil teks yang masuk akal sebagai definisi
            if teks_arti and len(teks_arti) > 5:
                hasil.append(f"{i}. {teks_arti}")
        
        if not hasil:
            return "Kata tidak ditemukan atau struktur web berubah."
            
        return "\n\n".join(hasil[:5]) # Ambil 5 arti teratas
        
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirimkan satu kata untuk mencari artinya di KBBI Kemendikdasmen.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kata = update.message.text
    await update.message.reply_text(f"Mencari arti kata: **{kata}**...", parse_mode='Markdown')
    
    definisi = scrape_kbbi(kata)
    await update.message.reply_text(f"**{kata}**:\n\n{definisi}", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot KBBI Berjalan...")
    app.run_polling()
