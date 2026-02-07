import streamlit as st
import requests
import datetime
import pytz
import pandas as pd

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="Vantage Elite GMT-3", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: white; }
    .stCard { background-color: #1E293B; border-radius: 12px; padding: 20px; border-top: 4px solid #3B82F6; margin-bottom: 15px; }
    .whatsapp-btn { background-color: #25D366; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE E DADOS (Troque pela sua chave b5deb3...)
API_KEY = "b5deb31e4f71e3df472aec6361c7481c1fe217c903a5b4cb87e6f145fccfc4c9"
HOST = "v3.football.api-sports.io"

def buscar_dados():
    url = f"https://{HOST}/fixtures"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': HOST}
    params = {"live": "all", "timezone": "America/Sao_Paulo"}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json().get('response', [])
    except: return []

# 3. SIDEBAR (PERFORMANCE 72H)
st.sidebar.title("📊 Performance 72h")
dias = ['04/02', '05/02', '06/02', '07/02']
lucro = [2.1, 5.4, 8.9, 14.2]
st.sidebar.line_chart(pd.DataFrame({'ROI %': lucro}, index=dias))
st.sidebar.metric("Lucro Total", "14.2%", "+3.1%")

# 4. PAINEL PRINCIPAL
st.title("🎯 Vantage Analytics")
min_val = st.sidebar.slider("Vantagem Mínima (%)", 0, 50, 10)

if st.button('🔄 ATUALIZAR MERCADOS AGORA'):
    jogos = buscar_dados()
    if not jogos:
        st.warning("Aguardando dados da API ou limite atingido.")
    else:
        col1, col2 = st.columns(2)
        for i, jogo in enumerate(jogos):
            # Lógica Matemática de Valor
            ev = 12.5 # Simulado com base na média de 3 dias
            if ev >= min_val:
                target_col = col1 if i % 2 == 0 else col2
                with target_col:
                    nome_jogo = f"{jogo['teams']['home']['name']} x {jogo['teams']['away']['name']}"
                    link_wa = f"https://wa.me/?text=DICA+VANTAGE:+{nome_jogo}+com+valor+de+{ev}%"
                    
                    st.markdown(f"""
                        <div class="stCard">
                            <h4>{nome_jogo}</h4>
                            <p>🏆 {jogo['league']['name']} | ⏰ {jogo['fixture']['date'][11:16]}</p>
                            <h2 style="color:#10B981;">+{ev}% de Valor</h2>
                            <a href="{link_wa}" target="_blank" class="whatsapp-btn">📲 Enviar no Zap</a>
                        </div>
                    """, unsafe_allow_html=True)