import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Pelonoli",
    page_icon="🌷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Gece Modu Üzerine Bordo & Pembe Vurgular (Lüks Tema)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* BAŞLIKLAR - Siyah ekranda parlayan Bordo/Pembe tonları */
    h1 {
        text-align: center;
        color: #d11a5a; 
        font-size: 32px;
        padding-bottom: 20px;
    }
    
    h4 {
        color: #ff9eaf; 
    }

    /* Primary Buton (Evet ve Devam Butonları) Bordo Rengi */
    button[kind="primary"] {
        background-color: #800020; 
        border: 1px solid #ff9eaf; 
        border-radius: 30px;
        height: 60px;
        width: 100%;
        transition: 0.3s;
    }
    
    button[kind="primary"] div, button[kind="primary"] p, button[kind="primary"] span {
        color: #ffffff; 
        font-size: 20px;
        font-weight: bold;
    }
    
    button[kind="primary"]:hover {
        background-color: #5c0016; 
        border-color: #ffffff;
    }
    
    /* Secondary Buton (Hayır Butonu) */
    button[kind="secondary"] {
        background-color: transparent;
        border: 2px solid #800020;
        border-radius: 30px;
        height: 60px;
        width: 100%;
    }
    
    button[kind="secondary"] div, button[kind="secondary"] p, button[kind="secondary"] span {
        color: #ff9eaf;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sayfa Geçişlerini Yönetmek İçin Session State
if 'adim' not in st.session_state:
    st.session_state.adim = 1

# --- ADIM 1: KARŞILAMA EKRANI ---
if st.session_state.adim == 1:
    st.title("Benimle date'e çıkar mısın Pelonoli? 🪷")
    
    st.write("")
    st.write("")
    
    st.markdown("<h4 style='text-align: center; font-weight: normal; margin-bottom: 30px;'>Hayır'a basmayı deneme bile :)</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Evet! 🌷", type="primary"):
            st.session_state.adim = 2
            st.session_state.balon_goster = True 
            st.rerun() 
            
    with col2:
        hayir_tiklandi = st.button("Hayır")
        
        if hayir_tiklandi:
            st.toast("Sana denememeni söylemiştim güzelim???", icon="🌷")

    components.html("""
        <script>
        const doc = window.parent.document;
        const buttons = Array.from(doc.querySelectorAll('button'));
        const hayirBtn = buttons.find(b => b.innerText.includes("Hayır"));
        
        if (hayirBtn) {
            hayirBtn.addEventListener('mouseover', function() {
                const x = Math.floor(Math.random() * 150); 
                const y = Math.floor(Math.random() * 300) - 150; 
                this.style.transform = `translate(${x}px, ${y}px)`;
                this.style.transition = "transform 0.15s ease-out";
            });
        }
        </script>
    """, height=0, width=0)


# --- ADIM 2: TAKVİM VE ZAMAN SEÇİMİ ---
elif st.session_state.adim == 2:
    
    if st.session_state.get('balon_goster', False):
        st.balloons()
        st.session_state.balon_goster = False

    st.title("Güzel bir başlangıç. 🌺")
    st.success("Zamanı belirleyelim.")
    
    st.write("Sana en uygun olan tarihi seçebilirsin:")
    
    bugun = datetime.date.today()
    secilen_tarih = st.date_input("Hangi gün?", min_value=bugun)
    
    secilen_sure = st.slider("Plan için ne kadar vaktimiz var? (Saat)", min_value=1.0, max_value=8.0, value=2.0, step=0.5)
    
    saat_secenekleri = [
        "16:00", "16:30", "17:00", "17:30", "18:00", 
        "18:30", "19:00", "19:30", "20:00", "20:30", "21:00"
    ]
    
    secilen_saat_str = st.selectbox("Saat kaçta başlayalım?", saat_secenekleri, index=4) 
    
    saat_int, dakika_int = map(int, secilen_saat_str.split(':'))
    baslangic_saati = datetime.time(saat_int, dakika_int)
    
    baslangic_dt = datetime.datetime.combine(bugun, baslangic_saati)
    bitis_dt = baslangic_dt + datetime.timedelta(hours=secilen_sure)
    
    st.info(f"O zaman planımız **{baslangic_saati.strftime('%H:%M')}** ile **{bitis_dt.strftime('%H:%M')}** arasında olacak. 🕰️")
    
    st.write("")
    if st.button("Devam Et ➡️", type="primary"):
        st.session_state.tarih = secilen_tarih
        st.session_state.sure = secilen_sure
        st.session_state.baslangic_saati = baslangic_saati.strftime('%H:%M')
        st.session_state.bitis_saati = bitis_dt.strftime('%H:%M')
        st.session_state.adim = 3
        st.rerun()


# --- ADIM 3: ETKİNLİK VE MEKAN SEÇİMİ ---
elif st.session_state.adim == 3:
    st.title("Günün Detayları 🪷")
    st.write("Peki bu sürede ne yapmayı tercih edersin?")
    
    etkinlik = st.radio(
        "Aktivite Seçimi:",
        ["Seçimini yap...", "🍔 Yemek", "☕ Kahve", "🍰 Tatlı", "🎬 Sinema", "🎳 Bowling / Oyun", "🤷‍♀️ Sana Bırakıyorum"]
    )
    
    mekan_secimi = None
    yemek_turu = None 
    
    # 1. YEMEK SEÇİMİ VE ALT MENÜLERİ
    if etkinlik == "🍔 Yemek":
        yemek_turu = st.selectbox(
            "Ne tür bir şeyler yemek istersin?", 
            ["Seçimini yap...", "Burger 🍔", "Pizza 🍕", "Döner 🥙", "Tantuni 🌯", "Makarna 🍝", "Fark Etmez, Sen Seç 🤷‍♀️"]
        )
        
        if yemek_turu == "Burger 🍔":
            mekan_secimi = st.selectbox("Mekan:", ["Seçimini yap...", "Mama's Burger", "Fel's Burger", "Burger King", "Popeyes", "Sen Seç 🌺"])
        elif yemek_turu == "Pizza 🍕":
            mekan_secimi = st.selectbox("Mekan:", ["Seçimini yap...", "Terra Pizza", "Evreka Pizza", "Express Lounge", "Sen Seç 🌺"])
        elif yemek_turu == "Döner 🥙":
            mekan_secimi = st.selectbox("Mekan:", ["Seçimini yap...", "Hatay Döner", "Öncü Döner", "Maydanoz Döner", "Sen Seç 🌺"])
        elif yemek_turu == "Tantuni 🌯":
            mekan_secimi = st.selectbox("Mekan:", ["Seçimini yap...", "Güler Tantuni", "Asel Tantuni", "Er Tantuni", "Hatıra Tantuni", "Mersin Tantuni", "Sen Seç 🌺"])
        elif yemek_turu == "Makarna 🍝":
            mekan_secimi = st.selectbox("Mekan:", ["Seçimini yap...", "Govala", "Chubby", "Le Monte", "Sen Seç 🌺"])
        elif yemek_turu == "Fark Etmez, Sen Seç 🤷‍♀️":
            mekan_secimi = "Sana Bırakıldı"

    # 2. KAHVE SEÇİMİ VE MEKANLARI
    elif etkinlik == "☕ Kahve":
        st.write("Güzel bir kahve eşliğinde sohbet... Nereyi istersin?")
        mekan_secimi = st.selectbox(
            "Mekan Tercihi:", 
            ["Seçimini yap...", "Heffalump", "Belize", "Wise", "Milklaç", "Starbucks", "Sen Seç 🌺"]
        )
        
    # 3. TATLI SEÇİMİ VE MEKANLARI
    elif etkinlik == "🍰 Tatlı":
        mekan_secimi = st.selectbox(
            "Tatlıcı Tercihi:", 
            ["Seçimini yap...", "Şebnem Pastanesi", "Milklaç", "Hb Waffle", "Lora", "Sen Seç 🌺"]
        )
        
    # 4. SİNEMA
    elif etkinlik == "🎬 Sinema":
        st.success("İnş vizyonda güzel bir film vardır. 🍿")
        mekan_secimi = "Sinema"

    # 5. BOWLING
    elif etkinlik == "🎳 Bowling / Oyun":
        st.success("Kazanacağını falan hiç düşünme ya söyleyeyim şimdiden. 🎳")
        mekan_secimi = "AVM (Park Karaman)"
        
    # 6. SANA BIRAKILDI
    elif etkinlik == "🤷‍♀️ Sana Bırakıyorum":
        st.success("Güzel bir plan hazırlayacağımdan emin olabilirsin. 🌺")
        mekan_secimi = "Sana Bırakıldı"

    # --- EKSTRA SEÇENEKLER VE NOT ALANI ---
    if mekan_secimi and mekan_secimi != "Seçimini yap...":
        st.write("---") 
        st.write("### Planı biraz daha zenginleştirelim mi? 🌷")
        
        ekstralar = st.multiselect(
            "Ana plandan sonra ne yapalım? (İsteğe bağlı)",
            [
                "☕ Birer kahve alırız",
                "🚶‍♀️ Temiz havada yürüyüş yaparız",
                "🌳 Açık havada oturup sohbet ederiz", 
                "🍦 Dondurma yeriz", 
                "🎬 Filme gireriz",
                "🏍️ Motorla biraz turlarız",
                "🗣️ Bol bol sohbet ederiz"
            ]
        )
        
        ekstra_not = st.text_area("Bana iletmek istediğin özel bir notun var mı? 📝", placeholder=" ÖRN= Mesela çok makara çocuksun, senden hoşlanmaya başladım, çok komiksin, sana çok gülüyorum, siteyi de çok beğendim seni de... ")
        
        st.write("")
        if st.button("Seçimleri Onayla 🌷", type="primary"):
            st.session_state.etkinlik = etkinlik
            st.session_state.yemek_turu = yemek_turu
            st.session_state.mekan = mekan_secimi
            st.session_state.ekstralar = ekstralar
            st.session_state.ekstra_not = ekstra_not
            st.session_state.adim = 4
            
            # --- TELEGRAM BİLDİRİM GÖNDERME KISMI ---
            TELEGRAM_BOT_TOKEN = "8964461758:AAGGOpesPBSuNMWJ49ZGEN7Mb1GfYxopA7w" 
            TELEGRAM_CHAT_ID = "1136831792"
            
            ekstra_metin = ", ".join(ekstralar) if ekstralar else "Seçilmedi"
            not_metin = ekstra_not if ekstra_not else "Yazılmadı"
            
            mesaj = f"""🚨 YENİ DATE ONAYLANDI! (Pelonoli) 🌺
📅 Tarih: {st.session_state.tarih.strftime('%d.%m.%Y')}
⏰ Saat: {st.session_state.baslangic_saati} - {st.session_state.bitis_saati}
🎯 Etkinlik: {etkinlik}
📍 Mekan: {mekan_secimi}
✨ Ekstralar: {ekstra_metin}
💌 Not: {not_metin}"""
            
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj}
                requests.post(url, data=payload)
            except Exception:
                pass 
            
            st.rerun()


# --- ADIM 4: SONUÇ VE BİLDİRİM EKRANI ---
elif st.session_state.adim == 4:
    st.balloons() 
    st.title("Plan Hazır! 🌷")
    st.write("İşte birlikte geçireceğimiz günün özeti:")
    
    st.success(f"**📅 Tarih:** {st.session_state.tarih.strftime('%d.%m.%Y')}")
    st.success(f"**⏰ Saat:** {st.session_state.baslangic_saati} - {st.session_state.bitis_saati}")
    
    if st.session_state.yemek_turu and st.session_state.yemek_turu != "Seçimini yap...":
        st.success(f"**🎯 Ne Yapıyoruz:** {st.session_state.etkinlik.split(' ', 1)[1]} ({st.session_state.yemek_turu.split(' ')[0]})")
    else:
        st.success(f"**🎯 Ne Yapıyoruz:** {st.session_state.etkinlik.split(' ', 1)[1]}")
        
    st.success(f"**📍 Mekan:** {st.session_state.mekan}")
    
    if st.session_state.ekstralar:
        ekstra_metin = ", ".join(st.session_state.ekstralar)
        st.info(f"**✨ Ekstra Planlar:** {ekstra_metin}")
        
    if st.session_state.ekstra_not:
        st.warning(f"**💌 Senin Notun:** {st.session_state.ekstra_not}")
    
    st.write("")
    st.error("Günün detayları başarıyla oluşturuldu. Bu sayfayı kaydedebilir veya ekran görüntüsü alabilirsin. Görüşmek üzere! 🌺")