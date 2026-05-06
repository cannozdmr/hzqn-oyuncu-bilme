import streamlit as st
import pandas as pd
import numpy as np
import os

# --- HIZLANDIRMA ÖZELLİĞİ (Caching) ---
# Bu fonksiyon veriyi bir kez okur ve hafızada tutar, siteyi hızlandırır.
@st.cache_data
def veriyi_yukle(dosya):
    if os.path.exists(dosya):
        df = pd.read_csv(dosya, sep=None, engine='python', encoding='latin1')
        df.columns = df.columns.str.strip()
        return df
    return None

# Sayfa Ayarları
st.set_page_config(page_title="CS Karakter Analizi v23", page_icon="🎯", layout="wide")

# --- HZQN LOGOSU (SOL ALT KÖŞE - SİYAH BEYAZ YUVARLAK) ---
st.markdown(
    """
    <style>
    .hzqn-logo {
        position: fixed;
        bottom: 30px;
        left: 30px;
        background-color: #1a1a1a;
        color: white;
        width: 110px;
        height: 110px;
        border-radius: 50%;
        font-size: 26px;
        font-weight: 900;
        z-index: 9999;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.7);
        border: 6px solid white;
        font-family: 'Arial Black', Gadget, sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
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
veri = veriyi_yukle(dosya_adi)

if veri is None:
    st.error(f"'{dosya_adi}' bulunamadı
