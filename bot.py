import yfinance as yf
import pandas as pd

def jalankan_robot_trading():
    print("=== ROBOT TRADING ETH/USDT BERKELANJUTAN ===")
    
    # 1. Ambil data historis
    data = yf.download("ETH-USD", period="60d", interval="1d", progress=False)
    
    df = pd.DataFrame()
    df['Close'] = data['Close']
    
    # 2. Menentukan Batas Kotak (Highest High & Lowest Low 10 periode sebelumnya)
    window = 10
    df['Box_High'] = df['Close'].shift(1).rolling(window=window).max()
    df['Box_Low'] = df['Close'].shift(1).rolling(window=window).min()
    
    # Ambil data hari terakhir
    harga_terkini = float(df['Close'].iloc[-1])
    atas_kotak = float(df['Box_High'].iloc[-1])
    
    print(f"Waktu Pengecekan  : Berhasil")
    print(f"Harga Terkini ETH : $ {harga_terkini:,.2f}")
    print(f"Atap Kotak (Res)  : $ {atas_kotak:,.2f}")
    print("-" * 45)
    
    # 3. Logika Keputusan Berdasarkan Teori Kotak
    if harga_terkini > atas_kotak:
        print("Keputusan Robot   : 🟢 BUY (Breakout terdeteksi!)")
        stop_loss = harga_terkini * (1 - 0.02)
        take_profit = harga_terkini * (1 + 0.04)
        print(f"👉 Target Take Profit : $ {take_profit:,.2f}")
        print(f"🛡️ Batas Stop Loss    : $ {stop_loss:,.2f}")
    else:
        print("Keputusan Robot   : 🔴 WAIT (Harga masih di dalam kotak, sabar menanti peluang)")

if __name__ == "__main__":
    jalankan_robot_trading()
