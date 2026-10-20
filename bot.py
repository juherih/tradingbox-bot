import yfinance as yf
import pandas as pd

def jalankan_robot_trading():
    print("=== SIMULASI ROBOT TRADING ETH/USDT (MODAL $50) ===")
    
    # 1. Konfigurasi Modal Awal Virtual
    modal_awal = 50.0  # dalam USD
    
    # 2. Ambil data historis
    data = yf.download("ETH-USD", period="60d", interval="1d", progress=False)
    
    df = pd.DataFrame()
    df['Close'] = data['Close']
    
    # 3. Menentukan Batas Kotak (Highest High & Lowest Low 10 periode sebelumnya)
    window = 10
    df['Box_High'] = df['Close'].shift(1).rolling(window=window).max()
    df['Box_Low'] = df['Close'].shift(1).rolling(window=window).min()
    
    # Ambil data hari terakhir
    harga_terkini = float(df['Close'].iloc[-1])
    atas_kotak = float(df['Box_High'].iloc[-1])
    
    print(f"Modal Virtual Awal : $ {modal_awal:,.2f}")
    print(f"Harga Terkini ETH  : $ {harga_terkini:,.2f}")
    print(f"Atap Kotak (Res)   : $ {atas_kotak:,.2f}")
    print("-" * 50)
    
    # 4. Logika Keputusan & Simulasi Alokasi Modal
    if harga_terkini > atas_kotak:
        print("Keputusan Robot    : 🟢 BUY (Breakout terdeteksi!)")
        
        # Simulasi pembelian aset dengan modal $50
        jumlah_eth = modal_awal / harga_terkini
        stop_loss = harga_terkini * (1 - 0.02)
        take_profit = harga_terkini * (1 + 0.04)
        
        print(f"👉 Alokasi Dibeli    : {jumlah_eth:.5f} ETH")
        print(f"🎯 Target Take Profit: $ {take_profit:,.2f} (+4%)")
        print(f"🛡️ Batas Stop Loss   : $ {stop_loss:,.2f} (-2%)")
    else:
        print("Keputusan Robot    : 🔴 WAIT (Harga masih di dalam kotak)")
        print("💡 Status Portofolio : Modal $50 aman dalam bentuk USDT (menunggu peluang breakout)")

if __name__ == "__main__":
    jalankan_robot_trading()
