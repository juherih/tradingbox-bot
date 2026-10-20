import os
import yfinance as yf
import pandas as pd
import urllib.request
import urllib.parse

def kirim_telegram(pesan):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("Token atau Chat ID Telegram belum diset!")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': pesan,
        'parse_mode': 'Markdown'
    }
    
    data = urllib.parse.urlencode(payload).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            print("Pesan Telegram berhasil terkirim!")
    except Exception as e:
        print(f"Gagal mengirim pesan Telegram: {e}")

def jalankan_robot_trading():
    print("=== SIMULASI ROBOT TRADING ETH/USDT + TELEGRAM ===")
    
    modal_awal = 50.0  # dalam USD
    
    # 1. Ambil data historis
    data = yf.download("ETH-USD", period="60d", interval="1d", progress=False)
    df = pd.DataFrame()
    df['Close'] = data['Close']
    
    # 2. Menentukan Batas Kotak (10 periode)
    window = 10
    df['Box_High'] = df['Close'].shift(1).rolling(window=window).max()
    df['Box_Low'] = df['Close'].shift(1).rolling(window=window).min()
    
    harga_terkini = float(df['Close'].iloc[-1])
    atas_kotak = float(df['Box_High'].iloc[-1])
    
    # 3. Susun Teks Laporan
    laporan = f"🤖 *LAPORAN ROBOT TRADING ETH/USDT*\n\n" \
              f"💰 Modal Virtual : *$ {modal_awal:,.2f}*\n" \
              f"📈 Harga Terkini : *$ {harga_terkini:,.2f}*\n" \
              f"📦 Atap Kotak    : *$ {atas_kotak:,.2f}*\n" \
              f"-----------------------------------\n"
    
    if harga_terkini > atas_kotak:
        jumlah_eth = modal_awal / harga_terkini
        stop_loss = harga_terkini * (1 - 0.02)
        take_profit = harga_terkini * (1 + 0.04)
        
        laporan += f"🟢 *KEPUTUSAN : BUY (Breakout!)*\n" \
                   f"👉 Alokasi : `{jumlah_eth:.5f} ETH`\n" \
                   f"🎯 TP : `$ {take_profit:,.2f}` (+4%)\n" \
                   f"🛡️ SL : `$ {stop_loss:,.2f}` (-2%)"
    else:
        laporan += f"🔴 *KEPUTUSAN : WAIT*\n" \
                   f"💡 Harga masih di dalam kotak, sabar menanti peluang breakout."

    print(laporan)
    
    # 4. Kirim ke Telegram
    kirim_telegram(laporan)

if __name__ == "__main__":
    jalankan_robot_trading()
