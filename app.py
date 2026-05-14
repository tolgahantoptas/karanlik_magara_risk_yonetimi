import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Karanlık Mağara", page_icon="💎")

# --- DURUM YÖNETİMİ ---
if 'banka' not in st.session_state:
    st.session_state.banka = 200
    st.session_state.envanter = {"Kalkan": 0, "Gözcü": 0, "Sıfırlayıcı": 0}
    st.session_state.giris_ucreti = 30
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.tuzak_orani = 0.20
    st.session_state.adim = 0
    st.session_state.mesaj = "Hoş geldin maceracı! Mağara seni bekliyor."
    st.session_state.gozcu_fısıltı = ""
    st.session_state.sandik_icerigi = None # BUGFIX: Kaderi burada tutuyoruz

# --- KADER BELİRLEME (BUGFIX ANAHTARI) ---
def kaderi_yaz():
    """Sandık açılmadan önce içeriği belirler, böylece Gözcü ile Aç butonu aynı veriye bakar."""
    st.session_state.sandik_icerigi = "TUZAK" if random.random() < st.session_state.tuzak_orani else "ALTIN"

def turu_bitir(kayip=False):
    if kayip:
        hasar = int(st.session_state.banka * 0.25)
        st.session_state.banka -= hasar
        st.session_state.mesaj = f"💥 TUZAK! Bankadan {hasar} altın gitti!"
    else:
        st.session_state.banka += st.session_state.tur_altini
        st.session_state.giris_ucreti += 15
        st.session_state.mesaj = f"🏦 {st.session_state.tur_altini} altın bankalandı!"
    
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.gozcu_fısıltı = ""
    st.session_state.sandik_icerigi = None

# --- YENİDEN BAŞLAT ---
def oyunu_sifirla():
    for key in st.session_state.keys(): del st.session_state[key]
    st.rerun()

# --- ARAYÜZ ---
st.title("💎 Karanlık Mağara")

# İflas Durumu
if st.session_state.banka < st.session_state.giris_ucreti and not st.session_state.tur_aktif:
    st.error(f"💀 İFLAS ETTİN! Banka: {st.session_state.banka}")
    if st.button("♻️ YENİDEN BAŞLA"): oyunu_sifirla()
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🎒 Durum")
    st.metric("Banka", f"{st.session_state.banka} 💰")
    st.write(f"🎫 Giriş: {st.session_state.giris_ucreti}")
    st.write("---")
    st.write("Envanter:", st.session_state.envanter)
    if st.button("🔄 Sıfırla"): oyunu_sifirla()

st.info(st.session_state.mesaj)

if not st.session_state.tur_aktif:
    # --- MAĞARA DIŞI (ESKİ TASARIM) ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Market")
        if st.button("🛡️ Kalkan Al (60)", help="Tuzaktan 1 kez korur."):
            if st.session_state.banka >= 60:
                st.session_state.banka -= 60
                st.session_state.envanter["Kalkan"] += 1
                st.rerun()
        if st.button("👁️ Gözcü Al (50)", help="Sandığa önceden bakar."):
            if st.session_state.banka >= 50:
                st.session_state.banka -= 50
                st.session_state.envanter["Gözcü"] += 1
                st.rerun()
        if st.button("🌀 Sıfırlayıcı Al (120)", help="Riski %20 yapar."):
            if st.session_state.banka >= 120:
                st.session_state.banka -= 120
                st.session_state.envanter["Sıfırlayıcı"] += 1
                st.rerun()
    with col2:
        st.subheader("🚪 Giriş")
        if st.button("🔥 MAĞARAYA GİR", type="primary"):
            st.session_state.banka -= st.session_state.giris_ucreti
            st.session_state.tur_aktif = True
            kaderi_yaz() # İlk sandığı belirle
            st.rerun()
else:
    # --- MAĞARA İÇİ (ESKİ TASARIM) ---
    adim = st.session_state.adim + 1
    kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
    hasar = int(st.session_state.banka * 0.25) + st.session_state.tur_altini
    
    st.subheader(f"📍 Adım: {adim}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tur Altını", st.session_state.tur_altini)
    c2.metric("Risk", f"%{int(st.session_state.tuzak_orani*100)}")
    c3.metric("Olası Kayıp", hasar)

    if st.session_state.gozcu_fısıltı: st.warning(st.session_state.gozcu_fısıltı)

    b1, b2, b3, b4 = st.columns(4)
    
    # SANDIĞI AÇ
    if b1.button("📦 AÇ"):
        if st.session_state.sandik_icerigi == "TUZAK":
            if st.session_state.envanter["Kalkan"] > 0:
                st.session_state.envanter["Kalkan"] -= 1
                st.session_state.mesaj = "🛡️ Kalkan seni korudu!"
                kaderi_yaz() # Yeni sandığı belirle
                st.rerun()
            else:
                turu_bitir(kayip=True)
                st.rerun()
        else:
            st.session_state.tur_altini += kazanc
            st.session_state.tuzak_orani += 0.07
            st.session_state.adim += 1
            st.session_state.gozcu_fısıltı = ""
            kaderi_yaz() # Bir sonraki sandığı belirle
            st.rerun()

    if b2.button("🏦 BANKALA"):
        turu_bitir(kayip=False)
        st.rerun()

    if b3.button("👁️ GÖZCÜ"):
        if st.session_state.envanter["Gözcü"] > 0:
            st.session_state.envanter["Gözcü"] -= 1
            guven = 0.8 if st.session_state.adim >= 7 else 1.0
            gercek = st.session_state.sandik_icerigi
            tahmin = gercek if random.random() <= guven else ("ALTIN" if gercek=="TUZAK" else "TUZAK")
            st.session_state.gozcu_fısıltı = f"Gözcü: '{tahmin}' (Güven: %{guven*100})"
            st.rerun()

    if b4.button("🌀 SIFIRLA"):
        if st.session_state.envanter["Sıfırlayıcı"] > 0:
            st.session_state.envanter["Sıfırlayıcı"] -= 1
            st.session_state.tuzak_orani = 0.20
            kaderi_yaz() # Risk değişince kaderi tekrar belirle
            st.rerun()