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
    st.session_state.sandik_icerigi = "TUZAK" if random.random() < st.session_state.tuzak_orani else "ALTIN"

def turu_bitir(kayip=False):
    if kayip:
        ceza = int(st.session_state.banka * 0.25)
        st.session_state.banka -= ceza
        st.session_state.mesaj = f"💥 TUZAK! {st.session_state.tur_altini} altın ve bankadan {ceza} altın (tedavi masrafı) kesildi!"
    else:
        st.session_state.banka += st.session_state.tur_altini
        st.session_state.giris_ucreti += 15
        st.session_state.mesaj = f"🏦 {st.session_state.tur_altini} altın bankalandı! Yeni giriş ücreti: {st.session_state.giris_ucreti}"
    
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
    st.session_state.sandik_icerigi = None
    st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎒 Oyuncu Bilgileri")
    st.metric("Banka Bakiyesi", f"{st.session_state.banka} 💰")
    st.write(f"🎫 **Giriş Ücreti:** {st.session_state.giris_ucreti}")
    st.write("---")
    st.subheader("Envanter")
    st.write(f"🛡️ **Kalkan:** {st.session_state.envanter['Kalkan']} adet")
    st.write(f"👁️ **Gözcü Kuşu:** {st.session_state.envanter['Gözcü']} adet")
    st.write(f"🌀 **Sıfırlayıcı:** {st.session_state.envanter['Sıfırlayıcı']} adet")
    st.write("---")
    st.button("🔄 OYUNU SIFIRLA", on_click=oyunu_sifirla, help="Tüm ilerlemeyi siler ve oyunu başlangıç durumuna döndürür.")

# --- ANA EKRAN ---
st.title("💎 Karanlık Mağara")

if st.session_state.banka < st.session_state.giris_ucreti and not st.session_state.tur_aktif:
    st.error(f"💀 İFLAS ETTİN! Bankanda sadece {st.session_state.banka} altın kaldı.")
    if st.button("♻️ YENİDEN BAŞLA", type="primary", help="Sermayen bittiğinde verilen acil durum fonuyla yeniden başlar."):
        oyunu_sifirla()
    st.stop()

# INTERAKTIF MESAJ PANELI
if "💥" in st.session_state.mesaj:
    st.error(st.session_state.mesaj)
elif "🏦" in st.session_state.mesaj or "✨" in st.session_state.mesaj:
    st.success(st.session_state.mesaj)
elif "🛡️" in st.session_state.mesaj or "🌀" in st.session_state.mesaj:
    st.warning(st.session_state.mesaj)
else:
    st.info(st.session_state.mesaj)

if not st.session_state.tur_aktif:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Market")
        # MOBİL UYUMLU BUTONLAR (Yardım Soru İşaretleri Eklendi)
        if st.button("🛡️ Kalkan Al (60)", help="Kalkan: Mağara içinde tuzağa yakalandığında banka hasarını bir kez %100 engeller.", use_container_width=True):
            if st.session_state.banka >= 60:
                st.session_state.banka -= 60
                st.session_state.envanter["Kalkan"] += 1
                st.session_state.mesaj = "🛡️ Kalkan satın alındı."
                st.rerun()
            else: st.error("Yetersiz bakiye!")
            
        if st.button("👁️ Gözcü Al (50)", help="Gözcü: Bir sonraki sandığın içeriğini kontrol eder. Derinlere inildikçe yanılma payı artar.", use_container_width=True):
            if st.session_state.banka >= 50:
                st.session_state.banka -= 50
                st.session_state.envanter["Gözcü"] += 1
                st.session_state.mesaj = "👁️ Gözcü Kuşu satın alındı."
                st.rerun()
            else: st.error("Yetersiz bakiye!")

        if st.button("🌀 Sıfırlayıcı Al (120)", help="Sıfırlayıcı: Biriken tuzak olasılığını başlangıç seviyesi olan %20'ye sabitler.", use_container_width=True):
            if st.session_state.banka >= 120:
                st.session_state.banka -= 120
                st.session_state.envanter["Sıfırlayıcı"] += 1
                st.session_state.mesaj = "🌀 Sıfırlayıcı satın alındı."
                st.rerun()
            else: st.error("Yetersiz bakiye!")

    with col2:
        st.subheader("🚪 Giriş")
        if st.button("🔥 MAĞARAYA GİR", type="primary", use_container_width=True, help="Giriş ücretini ödeyerek mağaraya girer. İçeride market kapalıdır."):
            st.session_state.banka -= st.session_state.giris_ucreti
            st.session_state.tur_aktif = True
            st.session_state.tuzak_orani = 0.20
            st.session_state.mesaj = "🔦 Mağaraya girildi. Dikkatli ilerle!"
            kaderi_yaz()
            st.rerun()
else:
    # --- MAĞARA İÇİ ---
    adim = st.session_state.adim + 1
    kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
    ceza_tahmini = int(st.session_state.banka * 0.25)
    hasar_gostergesi = ceza_tahmini + st.session_state.tur_altini
    
    st.subheader(f"📍 Adım: {adim}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tur Altını", st.session_state.tur_altini)
    c2.metric("Risk", f"%{int(st.session_state.tuzak_orani*100)}")
    c3.metric("Olası Kayıp", hasar_gostergesi)

    st.write(f"🎁 **Sıradaki Ödül:** {kazanc} Altın")

    if st.session_state.gozcu_fısıltı:
        st.warning(st.session_state.gozcu_fısıltı)

    # BUTONLAR MOBİL İÇİN container_width İLE AYARLANDI
    b1, b2 = st.columns(2)
    b3, b4 = st.columns(2)
    
    if b1.button("📦 AÇ", use_container_width=True, help=f"Risk al ve sandığı aç. Başarısızlık bankadan {ceza_tahmini} altın götürür."):
        if st.session_state.sandik_icerigi == "TUZAK":
            if st.session_state.envanter["Kalkan"] > 0:
                st.session_state.envanter["Kalkan"] -= 1
                st.session_state.mesaj = "🛡️ Kalkan seni korudu!"
                kaderi_yaz()
                st.rerun()
            else:
                turu_bitir(kayip=True)
                st.rerun()
        else:
            st.session_state.tur_altini += kazanc
            st.session_state.tuzak_orani += 0.07
            st.session_state.adim += 1
            st.session_state.mesaj = f"✨ Başarılı! +{kazanc} Altın."
            st.session_state.gozcu_fısıltı = ""
            kaderi_yaz()
            st.rerun()

    if b2.button("🏦 BANKALA", use_container_width=True, help="Toplam kazancı güvenli bankaya aktar ve mağaradan çık."):
        turu_bitir(kayip=False)
        st.rerun()

    if b3.button("👁️ GÖZCÜ", use_container_width=True, help="Gözcü Kuşu: Sıradaki sandığı mühürlenmiş kaderine göre kontrol eder."):
        if st.session_state.envanter["Gözcü"] > 0:
            st.session_state.envanter["Gözcü"] -= 1
            guven = 0.8 if st.session_state.adim >= 7 else 1.0
            gercek = st.session_state.sandik_icerigi
            tahmin = gercek if random.random() <= guven else ("ALTIN" if gercek=="TUZAK" else "TUZAK")
            st.session_state.gozcu_fısıltı = f"Gözcü: '{tahmin}' (Güven: %{guven*100})"
            st.rerun()
        else: st.error("Eşyan yok!")

    if b4.button("🌀 SIFIRLA", use_container_width=True, help="Sıfırlayıcı: Mevcut risk oranını %20'ye düşürür."):
        if st.session_state.envanter["Sıfırlayıcı"] > 0:
            st.session_state.envanter["Sıfırlayıcı"] -= 1
            st.session_state.tuzak_orani = 0.20
            st.session_state.mesaj = "🌀 Risk %20'ye sıfırlandı!"
            kaderi_yaz()
            st.rerun()
        else: st.error("Eşyan yok!")