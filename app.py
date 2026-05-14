import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Karanlık Mağara: Kesin Tahmin", page_icon="💎", layout="wide")

# --- SESSION STATE (DURUM YÖNETİMİ) ---
if 'banka' not in st.session_state:
    st.session_state.banka = 200
    st.session_state.envanter = {"Kalkan": 0, "Gözcü": 0, "Sıfırlayıcı": 0}
    st.session_state.giris_ucreti = 30
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.tuzak_orani = 0.20
    st.session_state.adim = 0
    st.session_state.mesaj = "Hazırsan mağaraya gir."
    st.session_state.gozcu_fısıltı = ""
    # KRİTİK DÜZELTME: Bir sonraki sandığın kaderini önceden belirle
    st.session_state.next_is_trap = False 

def oyunu_sifirla():
    st.session_state.banka = 200
    st.session_state.envanter = {"Kalkan": 0, "Gözcü": 0, "Sıfırlayıcı": 0}
    st.session_state.giris_ucreti = 30
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.mesaj = "Oyun sıfırlandı."
    st.session_state.gozcu_fısıltı = ""

def kaderi_belirle():
    """Bir sonraki sandığın içeriğini mevcut risk oranına göre önceden belirler."""
    st.session_state.next_is_trap = random.random() < st.session_state.tuzak_orani

def turu_bitir(kayip=False):
    if kayip:
        kritik_hasar = int(st.session_state.banka * 0.25)
        st.session_state.banka -= kritik_hasar
        st.session_state.mesaj = f"💥 PATLADIN! Bankadan {kritik_hasar} altın gitti!"
    else:
        st.session_state.banka += st.session_state.tur_altini
        st.session_state.giris_ucreti += 15
        st.session_state.mesaj = f"🏦 {st.session_state.tur_altini} altın bankalandı!"
    
    st.session_state.tur_aktif = False
    st.session_state.tur_altini = 0
    st.session_state.adim = 0
    st.session_state.gozcu_fısıltı = ""

# --- ANA EKRAN ---
st.title("💎 Karanlık Mağara")

is_broke = st.session_state.banka < st.session_state.giris_ucreti and not st.session_state.tur_aktif

if is_broke:
    st.error("💀 İFLAS ETTİN!")
    if st.button("♻️ YENİDEN BAŞLA"):
        oyunu_sifirla()
        st.rerun()
else:
    if not st.session_state.tur_aktif:
        # MARKET VE GİRİŞ
        st.info(st.session_state.mesaj)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🛒 Market")
            if st.button("🛡️ Kalkan Al (60)"):
                if st.session_state.banka >= 60:
                    st.session_state.banka -= 60
                    st.session_state.envanter["Kalkan"] += 1
                    st.rerun()
            if st.button("👁️ Gözcü Kuşu Al (50)"):
                if st.session_state.banka >= 50:
                    st.session_state.banka -= 50
                    st.session_state.envanter["Gözcü"] += 1
                    st.rerun()
        with col2:
            st.subheader("🚪 Mağara")
            if st.button("🔥 MAĞARAYA GİR"):
                st.session_state.banka -= st.session_state.giris_ucreti
                st.session_state.tur_aktif = True
                st.session_state.tuzak_orani = 0.20
                kaderi_belirle() # Mağaraya girerken ilk sandığı belirle
                st.rerun()
    else:
        # MAĞARA İÇİ
        adim = st.session_state.adim + 1
        kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
        hasar = int(st.session_state.banka * 0.25) + st.session_state.tur_altini
        
        st.subheader(f"📍 Adım: {adim} | Banka: {st.session_state.banka}")
        st.metric("Tur Altını", st.session_state.tur_altini, delta=f"Risk: %{int(st.session_state.tuzak_orani*100)}")

        if st.session_state.gozcu_fısıltı:
            st.warning(st.session_state.gozcu_fısıltı)

        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

        # AÇ BUTONU: Artık yeni zar atmıyor, önceden belirlenen kadere bakıyor
        if btn_col1.button("📦 SANDIĞI AÇ"):
            if st.session_state.next_is_trap:
                if st.session_state.envanter["Kalkan"] > 0:
                    st.session_state.envanter["Kalkan"] -= 1
                    st.session_state.mesaj = "🛡️ Kalkanın kırıldı!"
                    kaderi_belirle() # Kalkan sonrası yeni sandığı belirle
                    st.rerun()
                else:
                    turu_bitir(kayip=True)
                    st.rerun()
            else:
                st.session_state.tur_altini += kazanc
                st.session_state.tuzak_orani += 0.07
                st.session_state.adim += 1
                st.session_state.gozcu_fısıltı = ""
                kaderi_belirle() # Başarılı açılış sonrası bir sonrakini belirle
                st.rerun()

        if btn_col2.button("🏦 BANKALA"):
            turu_bitir(kayip=False)
            st.rerun()

        if btn_col3.button("👁️ GÖZCÜ"):
            if st.session_state.envanter["Gözcü"] > 0:
                st.session_state.envanter["Gözcü"] -= 1
                guven = 0.8 if st.session_state.adim >= 7 else 1.0
                
                # Gözcü, st.session_state.next_is_trap değerine göre fısıldar
                gercek = "TUZAK 💀" if st.session_state.next_is_trap else "ALTIN 💰"
                
                if random.random() > guven: # Güven sınırına göre yanıltma
                    tahmin = "ALTIN 💰" if gercek == "TUZAK 💀" else "TUZAK 💀"
                else:
                    tahmin = gercek
                    
                st.session_state.gozcu_fısıltı = f"Gözcü: '{tahmin}' (Güven: %{guven*100})"
                st.rerun()

        if btn_col4.button("🌀 SIFIRLA"):
            if st.session_state.envanter["Sıfırlayıcı"] > 0:
                st.session_state.envanter["Sıfırlayıcı"] -= 1
                st.session_state.tuzak_orani = 0.20
                kaderi_belirle() # Risk değiştiği için sandığı tekrar belirle
                st.rerun()