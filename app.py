import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Karanlık Mağara", page_icon="💎")

# --- DURUM YÖNETİMİ ---
def ilk_yukleme():
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

ilk_yukleme()

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
    # Session state'i tamamen temizleyip yeniden başlatıyoruz
    for key in list(st.session_state.keys()):
        del st.session_state[key]
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
    if st.button("🔄 OYUNU SIFIRLA", help="Tüm ilerlemeyi siler."):
        oyunu_sifirla()

# --- ANA EKRAN ---
st.title("💎 Karanlık Mağara")

if st.session_state.banka < st.session_state.giris_ucreti and not st.session_state.tur_aktif:
    st.error(f"💀 İFLAS ETTİN!")
    if st.button("♻️ YENİDEN BAŞLA", type="primary"):
        oyunu_sifirla()
    st.stop()

# MESAJ PANELI
if "💥" in st.session_state.mesaj: st.error(st.session_state.mesaj)
elif "🏦" in st.session_state.mesaj or "✨" in st.session_state.mesaj: st.success(st.session_state.mesaj)
elif "🛡️" in st.session_state.mesaj or "🌀" in st.session_state.mesaj: st.warning(st.session_state.mesaj)
else: st.info(st.session_state.mesaj)

if not st.session_state.tur_aktif:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Market")
        
        # Kalkan Alanı
        m1, m1h = st.columns([0.85, 0.15])
        if m1.button("🛡️ Kalkan Al (60)", use_container_width=True):
            if st.session_state.banka >= 60:
                st.session_state.banka -= 60
                st.session_state.envanter["Kalkan"] += 1
                st.session_state.mesaj = "🛡️ Kalkan satın alındı."
                st.rerun()
        m1h.button("❓", key="h_kalkan", help="Pasif Savunma: Mağara içinde tuzağa yakalandığınızda banka hasarını ve altın kaybını bir defaya mahsus %100 engeller.")

        # Gözcü Alanı
        m2, m2h = st.columns([0.85, 0.15])
        if m2.button("👁️ Gözcü Al (50)", use_container_width=True):
            if st.session_state.banka >= 50:
                st.session_state.banka -= 50
                st.session_state.envanter["Gözcü"] += 1
                st.session_state.mesaj = "👁️ Gözcü Kuşu satın alındı."
                st.rerun()
        m2h.button("❓", key="h_gozcu", help="İstihbarat: Bir sonraki sandığın içeriğini kontrol eder. Mağaranın derinliklerine inildikçe duyuları zayıflar ve yanılma payı artar.")

        # Sıfırlayıcı Alanı
        m3, m3h = st.columns([0.85, 0.15])
        if m3.button("🌀 Sıfırlayıcı Al (120)", use_container_width=True):
            if st.session_state.banka >= 120:
                st.session_state.banka -= 120
                st.session_state.envanter["Sıfırlayıcı"] += 1
                st.session_state.mesaj = "🌀 Sıfırlayıcı satın alındı."
                st.rerun()
        m3h.button("❓", key="h_sifir", help="Risk Yönetimi: Adım sayısı ilerledikçe biriken tuzak olasılığını kalıcı olarak başlangıç seviyesi olan %20'ye sabitler.")

    with col2:
        st.subheader("🚪 Giriş")
        g1, g1h = st.columns([0.85, 0.15])
        if g1.button("🔥 MAĞARAYA GİR", type="primary", use_container_width=True):
            st.session_state.banka -= st.session_state.giris_ucreti
            st.session_state.tur_aktif = True
            st.session_state.tuzak_orani = 0.20
            st.session_state.mesaj = "🔦 Mağara girildi. Dikkatli ilerle!"
            kaderi_yaz()
            st.rerun()
        g1h.button("❓", key="h_giris", help="Belirtilen giriş ücretini ödeyerek mağaraya girer. Mağara içinde markete erişim kapalıdır.")

else:
    # --- MAĞARA İÇİ ---
    adim = st.session_state.adim + 1
    kazanc = 20 if adim <= 3 else (50 if adim <= 6 else 150)
    ceza_tahmini = int(st.session_state.banka * 0.25)
    
    st.subheader(f"📍 Adım: {adim}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tur Altını", st.session_state.tur_altini)
    c2.metric("Risk", f"%{int(st.session_state.tuzak_orani*100)}")
    c3.metric("Olası Kayıp", ceza_tahmini + st.session_state.tur_altini)

    st.write(f"🎁 **Sıradaki Ödül:** {kazanc} Altın")
    if st.session_state.gozcu_fısıltı: st.warning(st.session_state.gozcu_fısıltı)

    # Aksiyon Butonları
    b1, b1h, b2, b2h = st.columns([0.4, 0.1, 0.4, 0.1])
    
    if b1.button("📦 AÇ", use_container_width=True):
        if st.session_state.sandik_icerigi == "TUZAK":
            if st.session_state.envanter["Kalkan"] > 0:
                st.session_state.envanter["Kalkan"] -= 1
                st.session_state.mesaj = "🛡️ Kalkan seni korudu!"
                kaderi_yaz(); st.rerun()
            else:
                turu_bitir(kayip=True); st.rerun()
        else:
            st.session_state.tur_altini += kazanc
            st.session_state.tuzak_orani += 0.07
            st.session_state.adim += 1
            st.session_state.mesaj = f"✨ Başarılı! +{kazanc} altın."
            kaderi_yaz(); st.rerun()
    b1h.button("❓", key="h_ac", help="Sandığı açar. Başarısızlık bankanın %25'ini ve tur altınlarını götürür.")

    if b2.button("🏦 BANKALA", use_container_width=True):
        turu_bitir(kayip=False); st.rerun()
    b2h.button("❓", key="h_bank", help="Kâr Realizasyonu: Toplanan altınları bankaya aktarır ve turu bitirir.")

    st.write("") # Boşluk
    b3, b3h, b4, b4h = st.columns([0.4, 0.1, 0.4, 0.1])

    if b3.button("👁️ GÖZCÜ", use_container_width=True):
        if st.session_state.envanter["Gözcü"] > 0:
            st.session_state.envanter["Gözcü"] -= 1
            guven = 0.8 if st.session_state.adim >= 7 else 1.0
            tahmin = st.session_state.sandik_icerigi if random.random() <= guven else ("ALTIN" if st.session_state.sandik_icerigi=="TUZAK" else "TUZAK")
            st.session_state.gozcu_fısıltı = f"Gözcü: '{tahmin}' (Güven: %{guven*100})"
            st.rerun()
    b3h.button("❓", key="h_goz_aktif", help="Aktif Yetenek: Bir sonraki sandığın içeriğine bakar.")

    if b4.button("🌀 SIFIRLA", use_container_width=True):
        if st.session_state.envanter["Sıfırlayıcı"] > 0:
            st.session_state.envanter["Sıfırlayıcı"] -= 1
            st.session_state.tuzak_orani = 0.20
            st.session_state.mesaj = "🌀 Mağara titreşimi azaldı, risk %20'ye sıfırlandı!"
            kaderi_yaz(); st.rerun()
    b4h.button("❓", key="h_sif_aktif", help="Stratejik Reset: Mevcut risk oranını %20'ye düşürür.")