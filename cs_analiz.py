import streamlit as st
import pandas as pd
import numpy as np
import os

# Sayfa Ayarları
st.set_page_config(page_title="CS Karakter Analizi v21", page_icon="🎯", layout="wide")

# --- HZQN LOGOSU (SOL ALT KÖŞE - SİYAH BEYAZ YUVARLAK) ---
st.markdown(
    """
    <style>
    .hzqn-logo {
        position: fixed;
        bottom: 30px;
        left: 30px;
        background-color: #1a1a1a; /* Siyah arka plan */
        color: white; /* Beyaz yazı */
        width: 110px; /* Genişlik */
        height: 110px; /* Yükseklik */
        border-radius: 50%; /* Tam yuvarlak */
        font-size: 26px;
        font-weight: 900;
        z-index: 9999;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.7);
        border: 6px solid white; /* Kalın beyaz çerçeve */
        font-family: 'Arial Black', Gadget, sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none; /* Mouse ile tıklanmayı engeller, formu kapatmaz */
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

# --- ANA UYGULAMA BAŞLIĞI ---
st.title("🎯 CS Arkadaş Tahmin Paneli")

dosya_adi = "arkadaslar.csv"

if not os.path.exists(dosya_adi):
    st.error(f"'{dosya_adi}' bulunamadı! Lütfen CSV dosyasını GitHub'a yüklediğinizden emin olun.")
else:
    try:
