import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Karanlık Mağara: Risk Yönetimi", page_icon="💎")

# --- SESSION STATE (DURUM YÖNETİMİ) ---
if 'banka' not in st.session_state:
    st.session_state.banka = 200
    st.session_state.envanter = {"Kalkan": 0, "Gözcü": 0, "Sıfırlayıcı": 0}
    st.session_state.giris_ucreti = 30
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.tuzak_orani = 0.20
    st.session_state.adim = 0
    st.session_state.mesaj = "Hoş geldin maceracı! Hazırsan mağaraya gir."
    if 'gozcu_fısıltı' not in st.session_state: st.session_state.gozcu_fısıltı = ""

# --- FONKSİYONLAR ---
def turu_bitir(kayip=False):
    if kayip:
        kritik_hasar = int(st.session_state.banka * 0.25)
        st.session_state.banka -= kritik_hasar
        st.session_state.mesaj = f"💥 PATLADIN! {st.session_state.tur_altini} altın ve bankadan {kritik_hasar} altın gitti!"
    else:
        st.session_state.banka += st.session_state.tur_altini
        st.session_state.giris_ucreti += 15
        st.session_state.mesaj = f"🏦 {st.session_state.tur_altini} altın bankalandı! Giriş ücreti arttı."
    
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.gozcu_fısıltı = ""

# --- ARAYÜZ (SIDEBAR) ---
with st.sidebar:
    st.header("🎒 Oyuncu Bilgileri")
    st.metric("Banka Bakiyesi", f"{st.session_state.banka} 💰")
    st.write(f"🎫 **Giriş Ücreti:** {st.session_state.giris_ucreti}")
    st.write("---")
    st.subheader("Envanter")
    for esya, adet in st.session_state.envanter.items():
        st.write(f"{esya}: {adet}")
    
    if st.button("❌ OYUNDAN ÇIK (QUIT)"):
        st.session_state.banka = 0
        st.warning("Maceradan çekildin. Oyun sıfırlandı.")
        st.stop()

# --- ANA EKRAN ---
st.title("💎 Karanlık Mağara")
st.info(st.session_state.mesaj)

if not st.session_state.tur_aktif:
    # --- MAĞARA DIŞI (MARKET VE GİRİŞ) ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛒 Market")
        if st.button("🛡️ Kalkan Al (60)"):
            if st.session_state.banka >= 60:
                st.session_state.banka -= 60
                st.session_state.envanter["Kalkan"] += 1
                st.rerun()
            else: st.error("Yetersiz altın!")
            
        if st.button("👁️ Gözcü Kuşu Al (50)"):
            if st.session_state.banka >= 50:
                st.session_state.banka -= 50
                st.session_state.envanter["Gözcü"] += 1
                st.rerun()
            else: st.error("Yetersiz altın!")

        if st.button("🌀 Sıfırlayıcı Al (120)"):
            if st.session_state.banka >= 120:
                st.session_state.banka -= 120
                st.session_state.envanter["Sıfırlayıcı"] += 1
                st.rerun()
            else: st.error("Yetersiz altın!")

    with col2:
        st.subheader("🚪 Mağara Kapısı")
        if st.button("🔥 MAĞARAYA GİR"):
            if st.session_state.banka >= st.session_state.giris_ucreti:
                st.session_state.banka -= st.session_state.giris_ucreti
                st.session_state.tur_aktif = True
                st.session_state.tuzak_orani = 0.20
                st.session_state.mesaj = "Mağaradasın! Her adımda risk artıyor."
                st.rerun()
            else:
                st.error("Giriş ücretini ödeyemiyorsun! İflas ettin.")

else:
    # --- MAĞARA İÇİ (OYUN AKIŞI) ---
    adim = st.session_state.adim + 1
    kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
    hasar = int(st.session_state.banka * 0.25) + st.session_state.tur_altini
    basari_sans = 1 - st.session_state.tuzak_orani
    ev = (basari_sans * kazanc) - (st.session_state.tuzak_orani * hasar)

    st.subheader(f"📍 Adım: {adim}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tur Altını", st.session_state.tur_altini)
    c2.metric("Tuzak Riski", f"%{int(st.session_state.tuzak_orani*100)}")
    c3.metric("Beklenen Değer (EV)", f"{ev:.2f}")

    if st.session_state.gozcu_fısıltı:
        st.warning(st.session_state.gozcu_fısıltı)

    st.write(f"🎁 **Sıradaki Sandık:** {kazanc} Altın | 💔 **Olası Kayıp:** {hasar}")

    btn1, btn2, btn3, btn4 = st.columns(4)

    if btn1.button("📦 SANDIĞI AÇ"):
        if random.random() < st.session_state.tuzak_orani:
            if st.session_state.envanter["Kalkan"] > 0:
                st.session_state.envanter["Kalkan"] -= 1
                st.session_state.mesaj = "🛡️ Kalkanın kırıldı ama hayattasın!"
                st.rerun()
            else:
                turu_bitir(kayip=True)
                st.rerun()
        else:
            st.session_state.tur_altini += kazanc
            st.session_state.tuzak_orani += 0.07
            st.session_state.adim += 1
            st.session_state.gozcu_fısıltı = ""
            st.session_state.mesaj = f"💰 {kazanc} altın buldun! Devam mı, tamam mı?"
            st.rerun()

    if btn2.button("🏦 BANKALA VE ÇIK"):
        turu_bitir(kayip=False)
        st.rerun()

    if btn3.button("👁️ GÖZCÜ KULLAN"):
        if st.session_state.envanter["Gözcü"] > 0:
            st.session_state.envanter["Gözcü"] -= 1
            guven = 0.8 if st.session_state.adim >= 7 else 1.0
            gercek = "TUZAK 💀" if random.random() < st.session_state.tuzak_orani else "ALTIN 💰"
            tahmin = gercek if random.random() <= guven else ("ALTIN" if gercek=="TUZAK" else "TUZAK")
            st.session_state.gozcu_fısıltı = f"Gözcü fısıldıyor: '{tahmin}' (Güven: %{guven*100})"
            st.rerun()
        else: st.error("Eşyan yok!")

    if btn4.button("🌀 SIFIRLA"):
        if st.session_state.envanter["Sıfırlayıcı"] > 0:
            st.session_state.envanter["Sıfırlayıcı"] -= 1
            st.session_state.tuzak_orani = 0.20
            st.session_state.mesaj = "Risk sıfırlandı!"
            st.rerun()
        else: st.error("Eşyan yok!")