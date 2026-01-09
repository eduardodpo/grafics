import streamlit as st
import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta
import pandas as pd

# ---------------------------------------------------
# CONFIGURAÇÕES INICIAIS
# ---------------------------------------------------
st.set_page_config(page_title="ETF Candlestick Viewer", layout="wide")

st.title(" Visualizador de Candlesticks para ETFs")
st.write("Selecione um ETF e o período para visualizar o gráfico.")

# Lista de ETFs da tua carteira
etfs = ["VOO", "QQQ", "VGT", "VT", "ACWI", "VTV", "XLV", "XLF", "IWM", "VGK", "EWJ", "INDA", "FXI"]

# Dropdowns
ticker = st.selectbox("Escolha o ETF:", etfs)
periodo = st.selectbox("Escolha o período:", ["5 anos", "1 ano", "6 meses"])

# ---------------------------------------------------
# DEFINIR DATAS
# ---------------------------------------------------
today = datetime.today()
periodos = {
    "5 anos": today - timedelta(days=365*5),
    "1 ano": today - timedelta(days=365),
    "6 meses": today - timedelta(days=182)
}

start_date = periodos[periodo]

# ---------------------------------------------------
# DOWNLOAD DOS DADOS
# ---------------------------------------------------
st.write(f"### Dados carregados para {ticker} — {periodo}")

etf = yf.Ticker(ticker)
data = etf.history(start=start_date, end=today)

if data.empty:
    st.error("Não foi possível carregar dados para este ETF.")
else:
    # ---------------------------------------------------
    # GERAR GRÁFICO CANDLE EM MEMÓRIA
    # ---------------------------------------------------
    fig = mpf.figure(style='yahoo', figsize=(12, 6))
    ax = fig.add_subplot(1,1,1)

    mpf.plot(
        data,
        type='candle',
        mav=(20, 50, 200),
        volume=True,
        ax=ax
    )

    # Mostrar no Streamlit
    st.pyplot(fig)