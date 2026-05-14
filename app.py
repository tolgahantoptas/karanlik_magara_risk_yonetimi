import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Karanlık Mağara: Risk Yönetimi", page_icon="💎", layout="wide")

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
    st.session_state.gozcu_fısıltı = ""

# --- YENİDEN BAŞLATMA FONKSİYONU ---
def oyunu_sifirla():
    st.session_state.banka = 200
    st.session_state.envanter = {"Kalkan": 0, "Gözcü": 0, "Sıfırlayıcı": 0}
    st.session_state.giris_ucreti = 30
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.mesaj = "Oyun sıfırlandı. Yeni macera başlasın!"
    st.session_state.gozcu_fısıltı = ""

def turu_bitir(kayip=False):
    if kayip:
        kritik_hasar = int(st.session_state.banka * 0.25)
        st.session_state.banka -= kritik_hasar
        st.session_state.mesaj = f"💥 PATLADIN! {st.session_state.tur_altini} altın ve bankadan {kritik_hasar} altın (tedavi masrafı) gitti!"
    else:
        st.session_state.banka += st.session_state.tur_altini
        st.session_state.giris_ucreti += 15
        st.session_state.mesaj = f"🏦 {st.session_state.tur_altini} altın bankalandı! Giriş ücreti arttı."
    
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.gozcu_fısıltı = ""

# --- İFLAS KONTROLÜ ---
is_broke = st.session_state.banka < st.session_state.giris_ucreti and not st.session_state.tur_aktif

# --- ARAYÜZ (SIDEBAR) ---
with st.sidebar:
    st.header("🎒 Oyuncu Bilgileri")
    st.metric("Banka Bakiyesi", f"{st.session_state.banka} 💰")
    st.write(f"🎫 **Giriş Ücreti:** {st.session_state.giris_ucreti}")
    st.write("---")
    st.subheader("Envanter")
    for esya, adet in st.session_state.envanter.items():
        st.write(f"{esya}: {adet}")
    
    st.write("---")
    if st.button("🔄 Oyunu Sıfırla", help="Tüm ilerlemeni siler ve baştan başlatır."):
        oyunu_sifirla()
        st.rerun()

# --- ANA EKRAN ---
st.title("💎 Karanlık Mağara")

if is_broke:
    st.error(f"💀 İFLAS ETTİN! Bankanda kalan: {st.session_state.banka} Altın. Giriş ücretini ödeyemiyorsun.")
    if st.button("♻️ YENİDEN BAŞLA", type="primary", use_container_width=True):
        oyunu_sifirla()
        st.rerun()
else:
    st.info(st.session_state.mesaj)

    if not st.session_state.tur_aktif:
        # --- MAĞARA DIŞI ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛒 Market")
            # help parametresi ile soru işaretli açıklamalar eklenir
            if st.button("🛡️ Kalkan Al (60)", help="Bir sonraki tuzağı engeller. Mağara içinde hayat kurtarır!", use_container_width=True):
                if st.session_state.banka >= 60:
                    st.session_state.banka -= 60
                    st.session_state.envanter["Kalkan"] += 1
                    st.rerun()
                else: st.error("Yetersiz altın!")
                
            if st.button("👁️ Gözcü Kuşu Al (50)", help="Bir sonraki sandığın içini fısıldar. 7. adımdan sonra yanılma payı %20'dir.", use_container_width=True):
                if st.session_state.banka >= 50:
                    st.session_state.banka -= 50
                    st.session_state.envanter["Gözcü"] += 1
                    st.rerun()
                else: st.error("Yetersiz altın!")

            if st.button("🌀 Sıfırlayıcı Al (120)", help="Mağaradaki mevcut tuzak oranını başlangıca (%20) çeker.", use_container_width=True):
                if st.session_state.banka >= 120:
                    st.session_state.banka -= 120
                    st.session_state.envanter["Sıfırlayıcı"] += 1
                    st.rerun()
                else: st.error("Yetersiz altın!")

        with col2:
            st.subheader("🚪 Mağara Kapısı")
            if st.button("🔥 MAĞARAYA GİR", type="primary", use_container_width=True):
                if st.session_state.banka >= st.session_state.giris_ucreti:
                    st.session_state.banka -= st.session_state.giris_ucreti
                    st.session_state.tur_aktif = True
                    st.session_state.tuzak_orani = 0.20
                    st.session_state.mesaj = "Mağaradasın! Her adımda risk artıyor."
                    st.rerun()

    else:
        # --- MAĞARA İÇİ ---
        adim = st.session_state.adim + 1
        kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
        hasar = int(st.session_state.banka * 0.25) + st.session_state.tur_altini
        
        st.subheader(f"📍 Adım: {adim}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Tur Altını", st.session_state.tur_altini)
        c2.metric("Tuzak Riski", f"%{int(st.session_state.tuzak_orani*100)}")
        c3.metric("Olası Kayıp", f"{hasar} 💔")

        if st.session_state.gozcu_fısıltı:
            st.warning(st.session_state.gozcu_fısıltı)

        st.write(f"🎁 **Sıradaki Ödül:** {kazanc} Altın")

        btn_col1, btn_col2 = st.columns(2)
        btn_col3, btn_col4 = st.columns(2)

        if btn_col1.button("📦 SANDIĞI AÇ", use_container_width=True):
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
                st.rerun()

        if btn_col2.button("🏦 BANKALA VE ÇIK", use_container_width=True):
            turu_bitir(kayip=False)
            st.rerun()

        if btn_col3.button("👁️ GÖZCÜ KULLAN", help="Sıradaki sandığı dikizler.", use_container_width=True):
            if st.session_state.envanter["Gözcü"] > 0:
                st.session_state.envanter["Gözcü"] -= 1
                guven = 0.8 if st.session_state.adim >= 7 else 1.0
                gercek = "TUZAK 💀" if random.random() < st.session_state.tuzak_orani else "ALTIN 💰"
                tahmin = gercek if random.random() <= guven else ("ALTIN" if gercek=="TUZAK" else "TUZAK")
                st.session_state.gozcu_fısıltı = f"Gözcü fısıldıyor: '{tahmin}' (Güven: %{guven*100})"
                st.rerun()
            else: st.error("Eşyan yok!")

        if btn_col4.button("🌀 SIFIRLA", help="Riski %20'ye çeker.", use_container_width=True):
            if st.session_state.envanter["Sıfırlayıcı"] > 0:
                st.session_state.envanter["Sıfırlayıcı"] -= 1
                st.session_state.tuzak_orani = 0.20
                st.session_state.mesaj = "Mağara sakinleşti (Risk %20)."
                st.rerun()
            else: st.error("Eşyan yok!")