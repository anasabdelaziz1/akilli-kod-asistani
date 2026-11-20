import streamlit as st
from google import genai
from google.genai import types

# 1. Sayfa Yapılandırması (Geniş Ekran ve Modern Görünüm)
st.set_page_config(
    page_title="AI Kod Asistanı & Konu Özetleyici",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Oturum geçmişini (Session State) başlatma
if "gecmis" not in st.session_state:
    st.session_state.gecmis = []
if "girdi_metni" not in st.session_state:
    st.session_state.girdi_metni = ""

# 2. Yan Menü (Sidebar) - Ayarlar ve Örnek Şablonlar
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg", width=45)
    st.title("Ayarlar & Kontroller")
    
    api_key = st.text_input(
        "🔑 Gemini API Anahtarı:",
        type="password",
        placeholder="API anahtarınızı yapıştırın..."
    )
    
    st.divider()
    st.subheader("⚙️ Analiz Parametreleri")
    
    dil_secimi = st.selectbox(
        "Programlama Dili / Bağlam:",
        ["Otomatik Algıla", "Python", "C#", "HTML / CSS / JS", "SQL", "Genel Akademik Metin"]
    )
    
    detay_seviyesi = st.select_slider(
        "Anlatım Seviyesi:",
        options=["Çok Kısa & Öz", "Orta (Standart)", "Detaylı & Öğretici"],
        value="Orta (Standart)"
    )

    st.divider()
    st.subheader("🧪 Hızlı Test Şablonları")
    st.caption("Hocaya sunum yaparken tek tıkla kutuyu doldurmak için kullanın:")
    
    if st.button("🐞 Örnek Hatalı Python Kodu", use_container_width=True):
        st.session_state.girdi_metni = (
            "def ortalama_hesapla(sayilar):\n"
            "    toplam = 0\n"
            "    for i in range(len(sayilar) + 1):\n"
            "        toplam += sayilar[i]\n"
            "    return toplam / len(sayilar)\n\n"
            "print(ortalama_hesapla([10, 20, 30]))"
        )
        
    if st.button("📚 Örnek Ders Metni (LLM)", use_container_width=True):
        st.session_state.girdi_metni = (
            "Büyük Dil Modelleri (LLM), milyarlarca parametreye sahip derin öğrenme "
            "algoritmaları kullanarak insan dilini anlayan, özetleyen ve üreten yapay zeka "
            "sistemleridir. Transformer mimarisi üzerine inşa edilen bu modeller, bağlam "
            "penceresi içerisindeki kelimeler arasındaki ilişkileri dikkat (attention) mekanizması "
            "sayesinde analiz eder."
        )

# 3. Ana Başlık Alanı
st.title("⚡ Akıllı Kod Asistanı & Konu Özetleyici")
st.markdown("*Yapay Zeka Destekli Kod Analizi, Hata Ayıklama (Debugging) ve Akademik Özetleme Platformu*")
st.divider()

# 4. Çift Sütunlu Çalışma Alanı (Sol: Giriş, Sağ: Sonuç)
sol_sutun, sag_sutun = st.columns([1, 1], gap="large")

with sol_sutun:
    st.subheader("📥 Girdi Alanı")
    
    islem_modu = st.radio(
        "Yapılacak İşlemi Seçin:",
        [
            "📝 Metni / Konuyu Özetle",
            "🔍 Kodu Satır Satır Açıkla",
            "🛠️ Koddaki Hataları Bul ve Düzelt",
            "⚡ Kodu Optimize Et (Daha Temiz Yaz)"
        ],
        horizontal=False
    )
    
    kullanici_girdisi = st.text_area(
        "Metin veya Kodunuz:",
        value=st.session_state.girdi_metni,
        height=300,
        placeholder="Buraya analiz edilecek kod bloğunu veya özetlenecek ders notunu yapıştırın..."
    )
    st.session_state.girdi_metni = kullanici_girdisi

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        calistir_butonu = st.button("🚀 Analizi Başlat", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🗑️ Temizle", use_container_width=True):
            st.session_state.girdi_metni = ""
            st.rerun()

with sag_sutun:
    st.subheader("📤 Yapay Zeka Çıktısı")
    
    if calistir_butonu:
        if not api_key:
            st.error("🔑 Lütfen sol menüden geçerli bir Gemini API Anahtarı girin.")
        elif not kullanici_girdisi.strip():
            st.warning("⚠️ Analiz edilecek bir metin veya kod girmediniz.")
        else:
            with st.spinner("Uygun Gemini modeli seçiliyor ve analiz yapılıyor..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    sistem_talimati = (
                        f"Sen uzman bir yazılım mühendisi ve üniversite düzeyinde sabırlı bir eğitmensin. "
                        f"Bağlam/Dil: {dil_secimi}. Anlatım seviyesi: {detay_seviyesi}. "
                        f"Yanıtlarını her zaman Türkçe, düzenli Markdown başlıkları ve temiz kod blokları kullanarak ver."
                    )
                    
                    if "Özetle" in islem_modu:
                        kullanici_istegi = f"Aşağıdaki metni ana fikirlerini kaybetmeden maddeler halinde özetle ve sonuna 3 maddelik 'Anahtar Kavramlar' bölümü ekle:\n\n{kullanici_girdisi}"
                    elif "Açıkla" in islem_modu:
                        kullanici_istegi = f"Aşağıdaki kodun amacını genel olarak özetle, ardından satır satır ne yaptığını öğretici bir dille açıkla:\n\n{kullanici_girdisi}"
                    elif "Hataları Bul" in islem_modu:
                        kullanici_istegi = f"Aşağıdaki koddaki sözdizimi (syntax) ve mantık (logic) hatalarını tespit et. Önce hatanın neden kaynaklandığını açıkla, sonra düzeltilmiş tam kodu paylaş:\n\n{kullanici_girdisi}"
                    else:
                        kullanici_istegi = f"Aşağıdaki kodu incele; daha performanslı, okunabilir ve modern yazılım standartlarına uygun (Clean Code) hale getirerek yapılan iyileştirmeleri açıkla:\n\n{kullanici_girdisi}"

                    # Hesabın erişebildiği tüm aktif Flash/Gemini modellerini otomatik bul
                    uygun_modeller = []
                    for m in client.models.list():
                        if "gemini" in m.name.lower() and "flash" in m.name.lower():
                            uygun_modeller.append(m.name)
                    
                    # Eğer flash bulunamazsa genel gemini modellerini ekle
                    if not uygun_modeller:
                        for m in client.models.list():
                            if "gemini" in m.name.lower():
                                uygun_modeller.append(m.name)

                    response = None
                    son_hata = None
                    kullanilan_model = ""

                    for secilen_model in uygun_modeller:
                        try:
                            response = client.models.generate_content(
                                model=secilen_model,
                                contents=kullanici_istegi,
                                config=types.GenerateContentConfig(
                                    system_instruction=sistem_talimati,
                                    temperature=0.3
                                )
                            )
                            kullanilan_model = secilen_model
                            break
                        except Exception as err:
                            son_hata = err
                            continue

                    if response is None:
                        raise Exception(f"Uygun model yanıt vermedi: {son_hata}")
                    
                    sonuc_metni = response.text
                    
                    # Geçmişe kaydet
                    st.session_state.gecmis.insert(0, {
                        "mod": islem_modu,
                        "girdi": kullanici_girdisi[:60] + "...",
                        "cikti": sonuc_metni
                    })
                    
                    st.success(f"✅ Analiz tamamlandı! (Kullanılan Model: {kullanilan_model})")
                    st.markdown(sonuc_metni)
                    
                    st.download_button(
                        label="💾 Sonucu Rapor Olarak İndir (.md)",
                        data=sonuc_metni,
                        file_name="ai_analiz_raporu.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"API Bağlantı Hatası: {e}")
    else:
        st.info("👈 Sol taraftan bir işlem seçip kodunuzu veya metninizi girerek **'Analizi Başlat'** butonuna basın.")

# 5. Alt Bölüm: Oturum Geçmişi
if st.session_state.gecmis:
    st.divider()
    st.subheader("🕒 Bu Oturumdaki İşlem Geçmişi")
    for idx, kayit in enumerate(st.session_state.gecmis):
        with st.expander(f"{idx + 1}. {kayit['mod']} — ({kayit['girdi']})"):
            st.markdown(kayit["cikti"])