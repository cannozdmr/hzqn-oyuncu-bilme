import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="CS Karakter Analizi v19", page_icon="🎯", layout="wide")

# --- HZQN LOGOSU (SOL ALT KÖŞE) ---
st.markdown(
    """
    <style>
    .hzqn-logo {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background-color: #ff4b4b; /* Kırmızı arka plan */
        color: white;
        padding: 15px 25px;
        border-radius: 50%; /* Yuvarlak yapma */
        font-size: 24px;
        font-weight: bold;
        z-index: 1000;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        border: 4px solid white;
        font-family: sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    <div class="hzqn-logo">HZQN</div>
    """,
    unsafe_allow_html=True
)

# --- KARŞILAMA MESAJI (MODAL) ---
@st.dialog("Bilgilendirme")
def hosgeldin_mesaji():
    st.write("### Merhaba!")
    st.info("Bu tahmin yapay zekası **Floki** tarafından yapılmıştır.")
    st.write("CS ekibimizden bir kişinin oynayış tarzını girin ve o kişiyi tahmin edeyim.")
    if st.button("Tamam", use_container_width=True):
        st.rerun()

if "mesaj_gosterildi" not in st.session_state:
    hosgeldin_mesaji()
    st.session_state["mesaj_gosterildi"] = True

# --- ANA UYGULAMA ---
st.title("🎯 CS Arkadaş Tahmin Paneli")

dosya_adi = "arkadaslar.csv"

if not os.path.exists(dosya_adi):
    st.error(f"'{dosya_adi}' bulunamadı!")
else:
    try:
        veri = pd.read_csv(dosya_adi, sep=None, engine='python', encoding='latin1')
        veri.columns = veri.columns.str.strip()
        
        ozellikler = ['oyun_tarzi', 'en_iyi_silah', 'info', 'aim', 'fav_map', 'oyun_saati', 'ekonomi']
        X = veri[ozellikler]
        y = veri['isim']

        def selector_format(option):
            return option[1]

        with st.form("final_logo_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                tarz = st.selectbox("Oyun Tarzı", options=[(0, "Seçiniz..."), (1,"Entry"),(2,"Lurk"),(3,"Dengeli"),(4,"Support")], format_func=selector_format, index=0)
                silah = st.selectbox("Favori Silah", options=[(0, "Seçiniz..."), (1,"AK-47"),(2,"AWP"),(5,"Zeus"),(6,"Baretta"),(7,"Hafif Makineli")], format_func=selector_format, index=0)
                ekonomi = st.selectbox("Ekonomi Yönetimi", options=[(-1, "Seçiniz..."), (1, "Yönetir"), (0, "Yönetemez")], format_func=selector_format, index=0)
            with c2:
                info = st.selectbox("İletişim", options=[(0, "Seçiniz..."), (1,"Sessiz"),(2,"Dengeli"),(3,"Çok Konuşur")], format_func=selector_format, index=0)
                harita = st.selectbox("En Sevdiği Harita", options=[(0, "Seçiniz..."), (1,"Mirage"),(2,"Inferno"),(3,"Dust2")], format_func=selector_format, index=0)
            with c3:
                saat = st.selectbox("Oyun Saati", options=[(0, "Seçiniz..."), (2,"Orta"),(3,"Yüksek")], format_func=selector_format, index=0)
                aim = st.slider("Aim Yeteneği", 1.0, 10.0, 5.0, step=0.1)
            
            submit = st.form_submit_button("ANALİZİ BAŞLAT")

        if submit:
            if tarz[0] == 0 or silah[0] == 0 or info[0] == 0 or harita[0] == 0 or saat[0] == 0 or ekonomi[0] == -1:
                st.warning("⚠️ Lütfen tüm seçenekleri doldurun!")
            else:
                girdi = np.array([tarz[0], silah[0], info[0], aim, harita[0], saat[0], ekonomi[0]])
                benzerlik_skorlari = []
                
                for index, row in X.iterrows():
                    farklar = []
                    oyuncu_verisi = row.values
                    for i in range(len(ozellikler)):
                        fark = abs(oyuncu_verisi[i] - girdi[i])
                        if i in [0, 1, 2, 4, 5, 6]: 
                            farklar.append(2.0 if fark != 0 else 0)
                        else:
                            farklar.append(fark / 2.5) 
                    
                    yuzde = 100 - (sum(farklar) * 14)
                    benzerlik_skorlari.append(max(0, yuzde))

                en_iyi_skor = max(benzerlik_skorlari)
                tahmin_edilen_kisi = y.iloc[np.argmax(benzerlik_skorlari)]

                st.divider()
                
                bilgi_notu = ""
                if tahmin_edilen_kisi == "Huseyin":
                    bilgi_notu = "Hüseyin, nam-ı değer HUSSOBEY bu! 👑"
                elif tahmin_edilen_kisi == "Yusuf":
                    bilgi_notu = "Zagreus bu sen misin? 🔥"
                elif tahmin_edilen_kisi == "Ibrahim":
                    bilgi_notu = "Hafif makineli diyorsun... İbrahim olabilir mi? 🤔" if silah[0] == 7 else "Mirage'ın gediklisi İbrahim Abi sahnede."
                elif tahmin_edilen_kisi == "Karanlik":
                    bilgi_notu = "Ekonomiyi yine batırmışız... Karanlık buralarda. 💸"
                else:
                    bilgi_notu = "Profil verileri bu arkadaşımızla eşleşiyor."

                st.success(f"### Tahmin Edilen: **{tahmin_edilen_kisi}**")
                st.write(f"📊 **Karakter Analiz Uyumu:** %{en_iyi_skor:.1f}")
                st.progress(en_iyi_skor / 100)
                st.info(f"💡 {bilgi_notu}")

    except Exception as e:
        st.error(f"Hata: {e}")
