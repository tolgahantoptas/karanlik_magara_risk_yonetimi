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
    st.session_state.sandik_icerigi = None 

# --- KADER BELİRLEME ---
def kaderi_yaz():
    """Sandık açılmadan önce içeriği belirler, Gözcü ile Aç butonunu senkronize eder."""
    st.session_state.sandik_icerigi = "TUZAK" if random.random() < st.session_state.tuzak_orani else "ALTIN"

def turu_bitir(kayip=False):
    if kayip:
        hasar = int(st.session_state.banka * 0.25)
        st.session_state.banka -= hasar
        st.session_state.mesaj = f"💥 TUZAK! Bankadan {hasar} altın (tedavi masrafı) kesildi!"
    else:
        st.session_state.banka += st.session_state.tur_altini
        st.session_state.giris_ucreti += 15
        st.session_state.mesaj = f"🏦 {st.session_state.tur_altini} altın bankalandı! Yeni girişi ücreti: {st.session_state.giris_ucreti}"
    
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.gozcu_fısıltı = ""
    st.session_state.sandik_icerigi = None

def oyunu_sifirla():
    st.session_state.banka = 200
    st.session_state.envanter = {"Kalkan": 0, "Gözcü": 0, "Sıfırlayıcı": 0}
    st.session_state.giris_ucreti = 30
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.tuzak_orani = 0.20
    st.session_state.mesaj = "Oyun sıfırlandı. Yeni macera başlasın!"
    st.session_state.gozcu_fısıltı = ""
    st.rerun()

# --- SIDEBAR (ENVANTER DÜZELTİLDİ) ---
with st.sidebar:
    st.header("🎒 Oyuncu Bilgileri")
    st.metric("Banka Bakiyesi", f"{st.session_state.banka} 💰")
    st.write(f"🎫 **Giriş Ücreti:** {st.session_state.giris_ucreti}")
    st.write("---")
    
    st.subheader("Envanter")
    # Eski listeleme formatına geri dönüldü
    st.write(f"🛡️ **Kalkan:** {st.session_state.envanter['Kalkan']} adet")
    st.write(f"👁️ **Gözcü Kuşu:** {st.session_state.envanter['Gözcü']} adet")
    st.write(f"🌀 **Sıfırlayıcı:** {st.session_state.envanter['Sıfırlayıcı']} adet")
    
    st.write("---")
    if st.button("🔄 OYUNU SIFIRLA"):
        oyunu_sifirla()

# --- ANA EKRAN ---
st.title("💎 Karanlık Mağara")

# İflas Kontrolü
if st.session_state.banka < st.session_state.giris_ucreti and not st.session_state.tur_aktif:
    st.error(f"💀 İFLAS ETTİN! Bankanda sadece {st.session_state.banka} altın kaldı.")
    if st.button("♻️ YENİDEN BAŞLA", type="primary"):
        oyunu_sifirla()
    st.stop()

st.info(st.session_state.mesaj)

if not st.session_state.tur_aktif:
    # --- MAĞARA DIŞI ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Market")
        if st.button("🛡️ Kalkan Al (60)", help="Tuzaktan 1 kez korur."):
            if st.session_state.banka >= 60:
                st.session_state.banka -= 60
                st.session_state.envanter["Kalkan"] += 1
                st.rerun()
            else: st.error("Yetersiz bakiye!")
            
        if st.button("👁️ Gözcü Al (50)", help="Sandığa önceden bakar."):
            if st.session_state.banka >= 50:
                st.session_state.banka -= 50
                st.session_state.envanter["Gözcü"] += 1
                st.rerun()
            else: st.error("Yetersiz bakiye!")

        if st.button("🌀 Sıfırlayıcı Al (120)", help="Riski %20'ye çeker."):
            if st.session_state.banka >= 120:
                st.session_state.banka -= 120
                st.session_state.envanter["Sıfırlayıcı"] += 1
                st.rerun()
            else: st.error("Yetersiz bakiye!")

    with col2:
        st.subheader("🚪 Giriş")
        if st.button("🔥 MAĞARAYA GİR", type="primary", use_container_width=True):
            st.session_state.banka -= st.session_state.giris_ucreti
            st.session_state.tur_aktif = True
            st.session_state.tuzak_orani = 0.20
            kaderi_yaz()
            st.rerun()
else:
    # --- MAĞARA İÇİ ---
    adim = st.session_state.adim + 1
    kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
    hasar = int(st.session_state.banka * 0.25) + st.session_state.tur_altini
    
    st.subheader(f"📍 Adım: {adim}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tur Altını", st.session_state.tur_altini)
    c2.metric("Risk", f"%{int(st.session_state.tuzak_orani*100)}")
    c3.metric("Olası Kayıp", hasar)

    if st.session_state.gozcu_fısıltı:
        st.warning(st.session_state.gozcu_fısıltı)

    b1, b2, b3, b4 = st.columns(4)
    
    if b1.button("📦 AÇ"):
        if st.session_state.sandik_icerigi == "TUZAK":
            if st.session_state.envanter["Kalkan"] > 0:
                st.session_state.envanter["Kalkan"] -= 1
                st.session_state.mesaj = "🛡️ Kalkanın kırıldı ama hayattasın!"
                kaderi_yaz()
                st.rerun()
            else:
                turu_bitir(kayip=True)
                st.rerun()
        else:
            st.session_state.tur_altini += kazanc
            st.session_state.tuzak_orani += 0.07
            st.session_state.adim += 1
            st.session_state.gozcu_fısıltı = ""
            kaderi_yaz()
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
        else: st.error("Eşyan yok!")

    if b4.button("🌀 SIFIRLA"):
        if st.session_state.envanter["Sıfırlayıcı"] > 0:
            st.session_state.envanter["Sıfırlayıcı"] -= 1
            st.session_state.tuzak_orani = 0.20
            kaderi_yaz()
            st.rerun()
        else: st.error("Eşyan yok!")