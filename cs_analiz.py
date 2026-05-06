import streamlit as st
import pandas as pd
import numpy as np
import os

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="CS Karakter Analizi Final", page_icon="🎮", layout="wide")

st.title("🎯 CS Arkadaş Tahmin Paneli - v10 (Final)")
st.markdown("Grubun oyun tarzını, tercihlerini ve ekonomi yönetimini analiz eden yapay zeka paneli.")

dosya_adi = "arkadaslar.csv"

if not os.path.exists(dosya_adi):
    st.error(f"Kritik Hata: '{dosya_adi}' dosyası bulunamadı! Lütfen dosyanın kodla aynı klasörde olduğundan emin olun.")
else:
    try:
        # Veriyi oku ve temizle
        veri = pd.read_csv(dosya_adi, sep=None, engine='python', encoding='latin1')
        veri.columns = veri.columns.str.strip()
        
        ozellikler = ['oyun_tarzi', 'en_iyi_silah', 'info', 'aim', 'fav_map', 'oyun_saati', 'ekonomi']
        X = veri[ozellikler]
        y = veri['isim']

        with st.form("final_analiz_formu"):
            c1, c2, c3 = st.columns(3)
            
            with c1:
                tarz = st.selectbox("Oyun Tarzı", 
                                   options=[(1,"Entry"),(2,"Lurk"),(3,"Dengeli"),(4,"Support")], 
                                   format_func=lambda x:x[1])
                silah = st.selectbox("Favori Silah", 
                                    options=[(1,"Tüfek"),(2,"AWP"),(5,"Zeus"),(6,"Baretta")], 
                                    format_func=lambda x:x[1])
                ekonomi = st.radio("Ekonomi Yönetimi", 
                                  options=[(1, "Ekonomisini Yönetir"), (0, "Yönetemez")], 
                                  format_func=lambda x: x[1])
            
            with c2:
                info = st.selectbox("İletişim / İnfo", 
                                   options=[(1,"Sessiz"),(2,"Dengeli"),(3,"Çok Konuşur")], 
                                   format_func=lambda x:x[1])
                harita = st.selectbox("En Sevdiği Harita", 
                                     options=[(1,"Mirage"),(2,"Inferno"),(3,"Dust2")], 
                                     format_func=lambda x:x[1])
            
            with c3:
                saat = st.selectbox("Oyun Saati", 
                                   options=[(2,"Orta"),(3,"Yüksek")], 
                                   format_func=lambda x:x[1])
                aim = st.slider("Aim Yeteneği (1-10)", 1.0, 10.0, 5.0, step=0.1)
            
            submit = st.form_submit_button("DETAYLI ANALİZİ BAŞLAT")

        if submit:
            # Girdi değerlerini diziye çevir
            girdi = np.array([tarz[0], silah[0], info[0], aim, harita[0], saat[0], ekonomi[0]])
            
            benzerlik_skorlari = []
            
            # Her oyuncu için benzerlik hesapla
            for index, row in X.iterrows():
                ceza_puanlari = []
                oyuncu_verisi = row.values
                
                for i in range(len(ozellikler)):
                    fark = abs(oyuncu_verisi[i] - girdi[i])
                    
                    # Kategorik veriler (Net tercihler) için sert ceza
                    if i in [0, 1, 2, 4, 5, 6]: 
                        if fark != 0:
                            ceza_puanlari.append(2.0) # Yanlış kategori seçimi %28 civarı düşürür
                        else:
                            ceza_puanlari.append(0)
                    else: # Aim (Sürekli veri) için yumuşak ceza
                        ceza_puanlari.append(fark / 2.0) 
                
                toplam_ceza = sum(ceza_puanlari)
                # Yüzdeyi hesapla ve %0-100 arasına çek
                yuzde = 100 - (toplam_ceza * 14)
                benzerlik_skorlari.append(max(2.5, yuzde))

            # En iyi sonucu bul
            en_iyi_skor = max(benzerlik_skorlari)
            tahmin_edilen_kisi = y.iloc[np.argmax(benzerlik_skorlari)]

            # Karakterlere özel küçük notlar
            bilgi_notu = ""
            if tahmin_edilen_kisi == "Karanlik" and ekonomi[0] == 0:
                bilgi_notu = "Ekonomi yönetimi zayıf ve Dust 2 aşığı... Bu kesin Karanlık! 💸"
            elif tahmin_edilen_kisi == "Yusuf" and aim > 8.0:
                bilgi_notu = "Bu keskin aim sadece Yusuf'ta olur. 🔥"
            elif tahmin_edilen_kisi == "Mustafa" and silah[0] == 2:
                bilgi_notu = "Sessiz ve AWP... Mustafa yine pusuda. 🎯"
            elif tahmin_edilen_kisi == "Ibrahim" and saat[0] == 2:
                bilgi_notu = "Orta seviye saat ve Mirage tutkusu İbrahim Abi'yi işaret ediyor. 🏰"
            else:
                bilgi_notu = "Girdiğiniz veriler en çok bu arkadaşımızla uyuşuyor."

            st.divider()
            
            # Sonuç Ekranı
            if en_iyi_skor > 70:
                st.balloons()
                st.success(f"### Tahmin Edilen Kişi: **{tahmin_edilen_kisi}**")
            else:
                st.warning(f"### En Yakın Profil: **{tahmin_edilen_kisi}**")
            
            st.write(f"📊 **Karakter Analiz Uyumu:** %{en_iyi_skor:.1f}")
            st.progress(en_iyi_skor / 100)
            st.info(f"💡 **Analiz Notu:** {bilgi_notu}")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")