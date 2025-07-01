import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import urllib.request
import json
import base64
import time
import re

# CONFIGURACIÓN MODERNA DE LA PÁGINA
st.set_page_config(
    page_title="🔮 Oráculo de Omaha - Buscador de Acciones Infravaloradas",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# FUNCIÓN PARA LOGO EMBEBIDO EN BASE64
def get_logo_base64(path="logo.png"):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

logo_base64 = get_logo_base64()

# HEADER PRINCIPAL CON LOGO EMBEBIDO
header_html = f"""
<div class="main-header" style="display: flex; align-items: center; justify-content: center; gap: 2rem; flex-wrap: wrap;">
    {'<img src="data:image/png;base64,' + logo_base64 + '" style="height:90px; border-radius:12px; box-shadow:0 2px 8px #0002; background:white; padding:8px;" alt="Logo"/>' if logo_base64 else '<span style="font-size:3rem;">🔮</span>'}
    <div style="text-align: center;">
        <h1 style="margin-bottom:0; color: white;">Oráculo de Omaha</h1>
        <p style="margin-top:0.5rem; color: white; opacity: 0.95;">Buscador de acciones infravaloradas e inspiración inversora</p>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# TEMA AZUL PROFESIONAL COMPLETO CON ANIMACIONES Y ESTILOS MEJORADOS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Roboto', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(30, 58, 138, 0.1), 0 10px 10px -5px rgba(30, 58, 138, 0.04);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main-header h1 {
        font-size: 3.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }

    .main-header p {
        font-size: 1.3rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2563eb;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .alert-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.1);
    }

    .success-alert {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 1px solid #10b981;
        color: #065f46;
    }

    .footer-container {
        background: linear-gradient(135deg, #f1f5f9 0%, #fff 100%);
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.1);
        animation: fadeInUp 0.8s ease-out 0.3s both;
    }

    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
    }

    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 8px;
    }

    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3);
    }

    .news-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }

    .news-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# CONFIGURACIÓN DE APIs
ALPHA_VANTAGE_API_KEY = "Z1VNLB6FJ0L0WSU0"
FMP_API_KEY = "qfhQA1pU9Vnx0JdfNiDaJf1sY08g2KhZ"

# LISTAS EXTENSAS DE TICKERS ORGANIZADAS POR MERCADO
SP500_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "TSLA", "BRK-B", "UNH", "JNJ", "XOM",
    "JPM", "V", "PG", "HD", "CVX", "MA", "BAC", "ABBV", "PFE", "AVGO",
    "KO", "MRK", "COST", "DIS", "WMT", "PEP", "TMO", "VZ", "ADBE", "NFLX",
    "CRM", "ABT", "NKE", "T", "ACN", "TXN", "LIN", "DHR", "QCOM", "NEE",
    "BMY", "PM", "RTX", "SPGI", "LOW", "UNP", "HON", "ORCL", "UPS", "IBM",
    "AMGN", "ELV", "SBUX", "CAT", "DE", "GS", "AXP", "BLK", "MDT", "GILD",
    "AMT", "CVS", "BKNG", "LRCX", "SYK", "TJX", "ADP", "VRTX", "MDLZ", "ADI",
    "ISRG", "C", "MMC", "ZTS", "PYPL", "REGN", "CB", "SO", "DUK", "BSX",
    "MO", "EOG", "ITW", "CSX", "WM", "PLD", "AON", "CL", "APD", "GE",
    "FDX", "SHW", "CME", "USB", "NSC", "GD", "TGT", "FCX", "EMR", "PSA"
]

IBEX35_TICKERS = [
    "SAN.MC", "BBVA.MC", "ITX.MC", "IBE.MC", "REP.MC", "TEF.MC", "AMS.MC", 
    "AENA.MC", "ANA.MC", "CABK.MC", "CLNX.MC", "COL.MC", "ELE.MC", "ENG.MC", 
    "FER.MC", "GRF.MC", "IAG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "MTS.MC",
    "NTGY.MC", "RED.MC", "ROVI.MC", "SAB.MC", "SCYR.MC", "SLR.MC", "UNI.MC",
    "VIS.MC", "ACX.MC", "ALM.MC", "BKT.MC", "CIE.MC", "FCC.MC", "FDR.MC"
]

MERCADOS_ASIATICOS_TICKERS = [
    # China Continental y Hong Kong
    "BABA", "JD", "PDD", "NTES", "BIDU", "NIO", "XPEV", "LI", "TME", "BILI",
    "700.HK", "9988.HK", "2318.HK", "1398.HK", "1299.HK", "3690.HK", "1810.HK",
    "0700.HK", "0941.HK", "1024.HK", "2382.HK", "3988.HK", "0388.HK",
    "600519.SS", "601318.SS", "601166.SS", "600036.SS", "601398.SS", "600028.SS",
    "000858.SZ", "000002.SZ", "000001.SZ", "002415.SZ", "300059.SZ",

    # Japón
    "6862.T", "8306.T", "9432.T", "6758.T", "7974.T", "9984.T", "6098.T", "8035.T",
    "4063.T", "6367.T", "7203.T", "6861.T", "8058.T", "9020.T", "4502.T",
    "4519.T", "8316.T", "9434.T", "4568.T", "6501.T", "7267.T", "8001.T",

    # Corea del Sur
    "005930.KS", "000660.KS", "066570.KS", "035420.KS", "068270.KS", "207940.KS",
    "005380.KS", "051910.KS", "006400.KS", "035720.KS", "028260.KS", "012330.KS",
    "003550.KS", "017670.KS", "096770.KS", "034730.KS", "018260.KS",

    # Taiwán
    "2382.TW", "2317.TW", "2454.TW", "2881.TW", "1303.TW", "2002.TW", "1216.TW",
    "2330.TW", "1301.TW", "2412.TW", "2308.TW", "1326.TW", "2886.TW",

    # India (ADRs)
    "INFY", "WIT", "HDB", "IBN", "TCOM", "VALE", "TSM", "UMC", "ASX", "RDY"
]

CRYPTO_TICKERS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD", "SOL-USD", "DOGE-USD",
    "DOT-USD", "AVAX-USD", "SHIB-USD", "MATIC-USD", "LTC-USD", "UNI-USD", "LINK-USD",
    "ATOM-USD", "ETC-USD", "XLM-USD", "BCH-USD", "ALGO-USD", "VET-USD", "ICP-USD",
    "FIL-USD", "TRX-USD", "EOS-USD", "AAVE-USD", "MKR-USD", "COMP-USD", "SUSHI-USD"
]

def obtener_tickers(indice):
    """Obtiene la lista de tickers según el índice seleccionado"""
    if indice == "S&P 500":
        return SP500_TICKERS
    elif indice == "IBEX 35":
        return IBEX35_TICKERS
    elif indice == "Mercados Asiáticos":
        return MERCADOS_ASIATICOS_TICKERS
    elif indice == "Criptomonedas":
        return CRYPTO_TICKERS
    else:
        return []

# SISTEMA DE CACHÉ MEJORADO CON PERSISTENCIA
cache_precios = {}
cache_datos_fundamentales = {}
CACHE_EXPIRATION_MINUTES = 5

def limpiar_cache():
    """Limpia el caché expirado"""
    current_time = datetime.now()
    keys_to_remove = []

    for key, (data, timestamp) in cache_precios.items():
        if (current_time - timestamp).total_seconds() > CACHE_EXPIRATION_MINUTES * 60:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del cache_precios[key]

def obtener_precio_alpha_vantage(ticker):
    """Obtiene el precio actual usando Alpha Vantage API con manejo de errores mejorado"""
    try:
        # Verificar caché
        if ticker in cache_precios:
            data, timestamp = cache_precios[ticker]
            if (datetime.now() - timestamp).total_seconds() < CACHE_EXPIRATION_MINUTES * 60:
                return data

        # Limpiar ticker para API
        ticker_clean = ticker.replace('.MC', '').replace('.HK', '').replace('.T', '').replace('.KS', '').replace('.TW', '').replace('.SS', '').replace('.SZ', '')

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker_clean}&apikey={ALPHA_VANTAGE_API_KEY}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            precio = float(data["Global Quote"]["05. price"])
            cache_precios[ticker] = (precio, datetime.now())
            return precio
        else:
            # Fallback a precio simulado si la API falla
            return obtener_precio_simple(ticker)

    except Exception as e:
        st.warning(f"Error obteniendo precio real para {ticker}: {str(e)}")
        return obtener_precio_simple(ticker)

def obtener_precio_simple(ticker):
    """Genera precios simulados realistas basados en datos históricos aproximados"""
    precios_demo = {
        # S&P 500 - Precios aproximados actuales
        "AAPL": 175.50, "MSFT": 380.25, "GOOGL": 140.75, "GOOG": 142.30, "AMZN": 145.30,
        "TSLA": 220.80, "BRK-B": 350.45, "UNH": 520.15, "JNJ": 165.80, "XOM": 110.75,
        "JPM": 150.45, "V": 245.60, "PG": 155.25, "HD": 310.90, "CVX": 160.40,
        "MA": 400.60, "BAC": 32.75, "ABBV": 150.45, "PFE": 35.80, "AVGO": 850.90,
        "KO": 55.30, "MRK": 120.60, "COST": 650.30, "DIS": 95.60, "WMT": 165.20,
        "PEP": 170.80, "TMO": 600.25, "VZ": 38.45, "ADBE": 485.90, "NFLX": 425.80,
        "CRM": 210.45, "ABT": 105.30, "NKE": 98.75, "T": 18.90, "ACN": 320.70,
        # IBEX 35 - Precios en euros
        "SAN.MC": 4.15, "BBVA.MC": 7.25, "ITX.MC": 28.60, "IBE.MC": 11.40, "REP.MC": 14.75,
        "TEF.MC": 4.30, "AMS.MC": 18.90, "AENA.MC": 145.60, "ANA.MC": 85.40, "CABK.MC": 4.85,
        "CLNX.MC": 30.25, "COL.MC": 15.70, "ELE.MC": 20.45, "ENG.MC": 40.80, "FER.MC": 25.35,
        "GRF.MC": 10.60, "IAG.MC": 2.45, "MAP.MC": 22.80, "MEL.MC": 8.25, "MRL.MC": 12.90,
        # Mercados Asiáticos
        "BABA": 85.40, "JD": 28.90, "PDD": 120.45, "NTES": 95.30, "BIDU": 110.75,
        "700.HK": 320.80, "9988.HK": 78.25, "2318.HK": 45.60, "1398.HK": 3.85, "1299.HK": 68.40,
        "TSM": 95.75, "6862.T": 40.75, "005930.KS": 140.45, "2382.TW": 200.45,
        "INFY": 18.90, "HDB": 65.30, "IBN": 22.45,
        # Criptomonedas
        "BTC-USD": 43250.80, "ETH-USD": 2650.45, "BNB-USD": 315.70, "XRP-USD": 0.62,
        "ADA-USD": 0.48, "SOL-USD": 98.35, "DOGE-USD": 0.085, "DOT-USD": 7.25,
        "AVAX-USD": 38.90, "SHIB-USD": 0.000024, "MATIC-USD": 0.85, "LTC-USD": 72.30
    }

    if ticker in precios_demo:
        # Añadir variación aleatoria pequeña para simular movimientos del mercado
        base_price = precios_demo[ticker]
        variation = np.random.uniform(-0.02, 0.02)  # ±2% de variación
        return round(base_price * (1 + variation), 6 if base_price < 1 else 2)
    else:
        # Para tickers no conocidos, generar precio basado en hash del ticker
        np.random.seed(hash(ticker) % 2**32)
        if ticker.endswith('-USD'):  # Crypto
            if 'SHIB' in ticker or 'DOGE' in ticker:
                precio_base = np.random.uniform(0.00001, 1)
            else:
                precio_base = np.random.uniform(0.01, 50000)
        elif ticker.endswith('.MC'):  # España
            precio_base = np.random.uniform(1, 100)
        elif ticker.endswith(('.HK', '.T', '.KS', '.TW', '.SS', '.SZ')):  # Asia
            precio_base = np.random.uniform(5, 500)
        else:  # US stocks
            precio_base = np.random.uniform(20, 800)
        return round(precio_base, 6 if precio_base < 1 else 2)

def calcular_indicadores_tecnicos(ticker, precio_actual):
    """Calcula indicadores técnicos simulados pero realistas"""
    np.random.seed(hash(ticker) % 2**32)

    # RSI (Relative Strength Index) - 0 a 100
    rsi = np.random.uniform(20, 80)

    # MACD - Puede ser positivo o negativo
    macd = np.random.uniform(-2, 2)

    # Bollinger Bands - Bandas superior e inferior
    bb_upper = precio_actual * np.random.uniform(1.02, 1.08)
    bb_lower = precio_actual * np.random.uniform(0.92, 0.98)

    # Moving Averages
    ma_20 = precio_actual * np.random.uniform(0.95, 1.05)
    ma_50 = precio_actual * np.random.uniform(0.90, 1.10)
    ma_200 = precio_actual * np.random.uniform(0.85, 1.15)

    # Volumen relativo
    volumen_relativo = np.random.uniform(0.5, 2.5)

    # Stochastic Oscillator
    stoch_k = np.random.uniform(10, 90)
    stoch_d = np.random.uniform(10, 90)

    return {
        'RSI': round(rsi, 1),
        'MACD': round(macd, 3),
        'BB_Upper': round(bb_upper, 2),
        'BB_Lower': round(bb_lower, 2),
        'MA_20': round(ma_20, 2),
        'MA_50': round(ma_50, 2),
        'MA_200': round(ma_200, 2),
        'Volumen_Relativo': round(volumen_relativo, 2),
        'Stoch_K': round(stoch_k, 1),
        'Stoch_D': round(stoch_d, 1)
    }

def obtener_datos_fundamentales(ticker):
    """Obtiene datos fundamentales simulados pero realistas"""
    np.random.seed(hash(ticker) % 2**32)

    # P/E Ratio - Varía según el tipo de empresa
    if ticker in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]:
        pe_ratio = np.random.uniform(15, 35)  # Tech giants
    elif ticker.endswith('.MC'):
        pe_ratio = np.random.uniform(8, 20)   # European stocks
    elif ticker.endswith('-USD'):
        pe_ratio = None  # Crypto no tiene P/E
    else:
        pe_ratio = np.random.uniform(10, 25)

    # Dividend Yield - Varía según el sector
    if ticker in ["KO", "PG", "JNJ", "VZ", "T"]:
        dividend_yield = np.random.uniform(2, 6)  # Dividend aristocrats
    elif ticker.endswith('-USD'):
        dividend_yield = 0  # Crypto no paga dividendos
    else:
        dividend_yield = np.random.uniform(0, 4)

    # Market Cap (en billones USD)
    if ticker in ["AAPL", "MSFT", "GOOGL", "AMZN"]:
        market_cap = np.random.uniform(1.5, 3.0)
    elif ticker.endswith('.MC'):
        market_cap = np.random.uniform(0.01, 0.1)
    elif ticker.endswith('-USD'):
        if ticker == "BTC-USD":
            market_cap = np.random.uniform(0.8, 1.2)
        elif ticker == "ETH-USD":
            market_cap = np.random.uniform(0.3, 0.5)
        else:
            market_cap = np.random.uniform(0.001, 0.1)
    else:
        market_cap = np.random.uniform(0.1, 1.0)

    # P/B Ratio
    pb_ratio = np.random.uniform(0.8, 4.5) if not ticker.endswith('-USD') else None

    # ROE (Return on Equity)
    roe = np.random.uniform(5, 25) if not ticker.endswith('-USD') else None

    # Debt to Equity
    debt_to_equity = np.random.uniform(0.1, 2.0) if not ticker.endswith('-USD') else None

    # EPS (Earnings Per Share)
    eps = np.random.uniform(1, 15) if not ticker.endswith('-USD') else None

    # Revenue Growth
    revenue_growth = np.random.uniform(-5, 25)

    return {
        'PE_Ratio': round(pe_ratio, 1) if pe_ratio else None,
        'Dividend_Yield': round(dividend_yield, 2),
        'Market_Cap': round(market_cap, 2),
        'PB_Ratio': round(pb_ratio, 1) if pb_ratio else None,
        'ROE': round(roe, 1) if roe else None,
        'Debt_to_Equity': round(debt_to_equity, 2) if debt_to_equity else None,
        'EPS': round(eps, 2) if eps else None,
        'Revenue_Growth': round(revenue_growth, 1)
    }

def obtener_datos_acciones(tickers, filtro_busqueda="", usar_api_real=False):
    """Obtiene y procesa datos de acciones con análisis completo"""

    # Diccionario de nombres de empresas
    nombres_empresas = {
        # S&P 500
        "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.", "GOOG": "Alphabet Inc. Class A",
        "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "BRK-B": "Berkshire Hathaway", "UNH": "UnitedHealth Group",
        "JNJ": "Johnson & Johnson", "XOM": "Exxon Mobil Corp.", "JPM": "JPMorgan Chase", "V": "Visa Inc.",
        "PG": "Procter & Gamble", "HD": "Home Depot", "CVX": "Chevron Corp.", "MA": "Mastercard Inc.",
        "BAC": "Bank of America", "ABBV": "AbbVie Inc.", "PFE": "Pfizer Inc.", "AVGO": "Broadcom Inc.",
        "KO": "Coca-Cola Company", "MRK": "Merck & Co.", "COST": "Costco Wholesale", "DIS": "Walt Disney Co.",
        "WMT": "Walmart Inc.", "PEP": "PepsiCo Inc.", "TMO": "Thermo Fisher Scientific", "VZ": "Verizon Communications",
        "ADBE": "Adobe Inc.", "NFLX": "Netflix Inc.", "CRM": "Salesforce Inc.", "ABT": "Abbott Laboratories",
        "NKE": "Nike Inc.", "T": "AT&T Inc.", "ACN": "Accenture PLC", "TXN": "Texas Instruments",

        # IBEX 35
        "SAN.MC": "Banco Santander", "BBVA.MC": "Banco Bilbao Vizcaya", "ITX.MC": "Inditex",
        "IBE.MC": "Iberdrola", "REP.MC": "Repsol", "TEF.MC": "Telefónica", "AMS.MC": "Amadeus IT Group",
        "AENA.MC": "Aena", "ANA.MC": "Acciona", "CABK.MC": "CaixaBank", "CLNX.MC": "Cellnex Telecom",
        "COL.MC": "Colonial", "ELE.MC": "Endesa", "ENG.MC": "Enagás", "FER.MC": "Ferrovial",
        "GRF.MC": "Grifols", "IAG.MC": "International Airlines Group", "MAP.MC": "Mapfre",
        "MEL.MC": "Meliá Hotels", "MRL.MC": "Merlin Properties", "MTS.MC": "ArcelorMittal",

        # Mercados Asiáticos
        "BABA": "Alibaba Group", "JD": "JD.com Inc.", "PDD": "PDD Holdings", "NTES": "NetEase Inc.",
        "BIDU": "Baidu Inc.", "NIO": "NIO Inc.", "XPEV": "XPeng Inc.", "LI": "Li Auto Inc.",
        "TSM": "Taiwan Semiconductor", "700.HK": "Tencent Holdings", "9988.HK": "Alibaba Group (HK)",
        "005930.KS": "Samsung Electronics", "000660.KS": "SK Hynix", "2330.TW": "Taiwan Semiconductor",
        "INFY": "Infosys Limited", "HDB": "HDFC Bank", "IBN": "ICICI Bank",

        # Criptomonedas
        "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "BNB-USD": "Binance Coin", "XRP-USD": "XRP",
        "ADA-USD": "Cardano", "SOL-USD": "Solana", "DOGE-USD": "Dogecoin", "DOT-USD": "Polkadot",
        "AVAX-USD": "Avalanche", "SHIB-USD": "Shiba Inu", "MATIC-USD": "Polygon", "LTC-USD": "Litecoin"
    }

    # Filtrar tickers si hay búsqueda
    if filtro_busqueda:
        tickers_filtrados = []
        filtro_lower = filtro_busqueda.lower()
        for ticker in tickers:
            nombre = nombres_empresas.get(ticker, ticker).lower()
            if filtro_lower in ticker.lower() or filtro_lower in nombre:
                tickers_filtrados.append(ticker)
        tickers = tickers_filtrados

    if len(tickers) == 0:
        return pd.DataFrame()

    # Limpiar caché expirado
    limpiar_cache()

    datos = []

    # Multiplicadores de precio objetivo (simulan análisis de analistas)
    multiplicadores_objetivo = [1.05, 1.12, 1.28, 1.35, 1.08, 1.45, 1.18, 1.22, 1.38, 1.15,
                              1.25, 1.33, 1.42, 1.16, 1.29, 1.31, 1.19, 1.27, 1.41, 1.13,
                              1.21, 1.36, 1.14, 1.26, 1.39, 1.17, 1.24, 1.32, 1.43, 1.11]

    # Mostrar progreso
    progress_container = st.empty()

    for i, ticker in enumerate(tickers[:50]):  # Limitar a 50 para rendimiento
        # Mostrar progreso con estilo
        progress_html = f"""
        <div class="progress-container">
            <h4>🔍 Analizando {ticker}... ({i+1}/{min(len(tickers), 50)})</h4>
            <div style="background: #e5e7eb; border-radius: 10px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #2563eb, #3b82f6); height: 8px; width: {((i+1)/min(len(tickers), 50))*100}%; transition: width 0.3s ease;"></div>
            </div>
            <p style="margin-top: 0.5rem; color: #6b7280;">Empresa: {nombres_empresas.get(ticker, ticker)}</p>
        </div>
        """
        progress_container.markdown(progress_html, unsafe_allow_html=True)

        # Obtener precio actual
        if usar_api_real:
            precio = obtener_precio_alpha_vantage(ticker)
        else:
            precio = obtener_precio_simple(ticker)

        # Calcular precio objetivo y ganancia potencial
        multiplicador = multiplicadores_objetivo[i % len(multiplicadores_objetivo)]
        precio_objetivo = precio * multiplicador
        ganancia_potencial = ((precio_objetivo - precio) / precio) * 100

        # Obtener datos fundamentales y técnicos
        fundamentales = obtener_datos_fundamentales(ticker)
        tecnicos = calcular_indicadores_tecnicos(ticker, precio)

        # Determinar recomendación y color
        if ganancia_potencial > 30:
            color = '#059669'
            recomendacion = "🚀 COMPRA FUERTE"
            emoji_trend = "🚀"
        elif ganancia_potencial > 20:
            color = '#10b981'
            recomendacion = "📈 COMPRA"
            emoji_trend = "📈"
        elif ganancia_potencial > 10:
            color = '#f59e0b'
            recomendacion = "⚖️ MANTENER"
            emoji_trend = "⚖️"
        elif ganancia_potencial > 0:
            color = '#f97316'
            recomendacion = "⚠️ PRECAUCIÓN"
            emoji_trend = "⚠️"
        else:
            color = '#dc2626'
            recomendacion = "📉 VENDER"
            emoji_trend = "📉"

        # Formatear ganancia potencial con color
        ganancia_coloreada = f'<span style="color: {color}; font-weight: bold;">{ganancia_potencial:.1f}%</span>'
        recomendacion_coloreada = f'<span style="color: {color}; font-weight: bold;">{recomendacion}</span>'

        # Análisis técnico RSI
        if tecnicos['RSI'] < 30:
            señal_tecnica = '<span style="color: #059669; font-weight: bold;">🔥 SOBREVENTA</span>'
            rsi_color = '#059669'
        elif tecnicos['RSI'] > 70:
            señal_tecnica = '<span style="color: #dc2626; font-weight: bold;">❄️ SOBRECOMPRA</span>'
            rsi_color = '#dc2626'
        else:
            señal_tecnica = '<span style="color: #6b7280;">➡️ NEUTRAL</span>'
            rsi_color = '#6b7280'

        # Análisis de medias móviles
        if precio > tecnicos['MA_20'] > tecnicos['MA_50']:
            tendencia_ma = '<span style="color: #059669; font-weight: bold;">📈 ALCISTA</span>'
        elif precio < tecnicos['MA_20'] < tecnicos['MA_50']:
            tendencia_ma = '<span style="color: #dc2626; font-weight: bold;">📉 BAJISTA</span>'
        else:
            tendencia_ma = '<span style="color: #f59e0b; font-weight: bold;">➡️ LATERAL</span>'

        # Agregar datos a la lista
        datos.append({
            'Ticker': ticker,
            'Empresa': nombres_empresas.get(ticker, ticker),
            'Precio Actual': f"${precio:.2f}" if precio >= 1 else f"${precio:.6f}",
            'Precio Objetivo': f"${precio_objetivo:.2f}" if precio_objetivo >= 1 else f"${precio_objetivo:.6f}",
            'Ganancia Potencial': ganancia_coloreada,
            'Recomendación': recomendacion_coloreada,
            'P/E Ratio': fundamentales['PE_Ratio'] if fundamentales['PE_Ratio'] else 'N/A',
            'Dividend Yield': f"{fundamentales['Dividend_Yield']:.2f}%" if fundamentales['Dividend_Yield'] > 0 else 'N/A',
            'RSI': f'<span style="color: {rsi_color}; font-weight: bold;">{tecnicos["RSI"]:.1f}</span>',
            'Señal Técnica': señal_tecnica,
            'MA 20': f"${tecnicos['MA_20']:.2f}" if tecnicos['MA_20'] >= 1 else f"${tecnicos['MA_20']:.6f}",
            'MA 50': f"${tecnicos['MA_50']:.2f}" if tecnicos['MA_50'] >= 1 else f"${tecnicos['MA_50']:.6f}",
            'Tendencia MA': tendencia_ma,
            'Market Cap (B)': f"${fundamentales['Market_Cap']:.2f}B",
            'ROE': f"{fundamentales['ROE']:.1f}%" if fundamentales['ROE'] else 'N/A',
            'Revenue Growth': f"{fundamentales['Revenue_Growth']:.1f}%",
            'Volumen Rel.': f"{tecnicos['Volumen_Relativo']:.1f}x"
        })

        # Pequeña pausa para APIs reales
        if usar_api_real:
            time.sleep(0.1)

    # Limpiar indicador de progreso
    progress_container.empty()

    return pd.DataFrame(datos)

def crear_grafico_rendimiento(df):
    """Crea gráfico de barras con el rendimiento potencial"""
    try:
        if df.empty:
            return None

        # Extraer valores numéricos de ganancia potencial
        ganancias = []
        tickers = []
        for _, row in df.iterrows():
            try:
                # Extraer número de la cadena HTML
                ganancia_str = row['Ganancia Potencial']
                ganancia_num = float(re.search(r'([-+]?\d*\.?\d+)', ganancia_str).group(1))
                ganancias.append(ganancia_num)
                tickers.append(row['Ticker'])
            except:
                continue

        if not ganancias:
            return None

        # Crear gráfico
        fig, ax = plt.subplots(figsize=(12, 6))

        # Colores según ganancia
        colores = ['#059669' if g > 20 else '#10b981' if g > 10 else '#f59e0b' if g > 0 else '#dc2626' for g in ganancias]

        bars = ax.bar(range(len(tickers)), ganancias, color=colores, alpha=0.8)

        # Personalización
        ax.set_title('Ganancia Potencial por Acción', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Acciones', fontsize=12)
        ax.set_ylabel('Ganancia Potencial (%)', fontsize=12)
        ax.set_xticks(range(len(tickers)))
        ax.set_xticklabels(tickers, rotation=45, ha='right')

        # Línea horizontal en 0
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)

        # Añadir valores en las barras
        for bar, ganancia in zip(bars, ganancias):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
                   f'{ganancia:.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                   fontsize=8, fontweight='bold')

        plt.tight_layout()
        return fig

    except Exception as e:
        st.error(f"Error creando gráfico de rendimiento: {str(e)}")
        return None

def crear_grafico_sectorial(df):
    """Crea gráfico de distribución de recomendaciones"""
    try:
        if df.empty:
            return None

        # Contar recomendaciones
        recomendaciones = {}
        for _, row in df.iterrows():
            rec = row['Recomendación']
            # Extraer texto limpio de HTML
            rec_clean = re.sub(r'<[^>]+>', '', rec)
            if 'COMPRA FUERTE' in rec_clean:
                key = 'Compra Fuerte'
            elif 'COMPRA' in rec_clean:
                key = 'Compra'
            elif 'MANTENER' in rec_clean:
                key = 'Mantener'
            elif 'PRECAUCIÓN' in rec_clean:
                key = 'Precaución'
            elif 'VENDER' in rec_clean:
                key = 'Vender'
            else:
                key = 'Otros'

            recomendaciones[key] = recomendaciones.get(key, 0) + 1

        if not recomendaciones:
            return None

        # Crear gráfico de pastel
        fig, ax = plt.subplots(figsize=(8, 8))

        labels = list(recomendaciones.keys())
        sizes = list(recomendaciones.values())
        colors = ['#059669', '#10b981', '#f59e0b', '#f97316', '#dc2626'][:len(labels)]

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'fontsize': 10})

        # Personalización
        ax.set_title('Distribución de Recomendaciones', fontsize=16, fontweight='bold', pad=20)

        # Mejorar legibilidad
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        return fig

    except Exception as e:
        st.error(f"Error creando gráfico sectorial: {str(e)}")
        return None

# SISTEMA DE ALERTAS PERSONALIZADAS MEJORADO
def inicializar_alertas():
    """Inicializa el sistema de alertas en session_state"""
    if 'alertas' not in st.session_state:
        st.session_state.alertas = []
    if 'historial_alertas' not in st.session_state:
        st.session_state.historial_alertas = []

def agregar_alerta(ticker, precio_objetivo, tipo_alerta, comentario=""):
    """Agrega una nueva alerta al sistema"""
    nueva_alerta = {
        'ticker': ticker,
        'precio_objetivo': precio_objetivo,
        'tipo': tipo_alerta,
        'comentario': comentario,
        'fecha_creacion': datetime.now(),
        'activa': True,
        'id': len(st.session_state.alertas)
    }
    st.session_state.alertas.append(nueva_alerta)

def verificar_alertas(df):
    """Verifica si alguna alerta se ha activado"""
    alertas_activadas = []

    for i, alerta in enumerate(st.session_state.alertas):
        if not alerta['activa']:
            continue

        # Buscar el ticker en el DataFrame
        ticker_data = df[df['Ticker'] == alerta['ticker']]
        if not ticker_data.empty:
            # Extraer precio actual (remover $ y convertir a float)
            precio_actual_str = ticker_data.iloc[0]['Precio Actual']
            precio_actual = float(precio_actual_str.replace('$', ''))

            # Verificar condiciones de alerta
            if alerta['tipo'] == 'subida' and precio_actual >= alerta['precio_objetivo']:
                alertas_activadas.append({
                    'ticker': alerta['ticker'],
                    'precio_actual': precio_actual,
                    'precio_objetivo': alerta['precio_objetivo'],
                    'tipo': 'subida',
                    'comentario': alerta.get('comentario', '')
                })
                # Desactivar alerta y mover al historial
                st.session_state.alertas[i]['activa'] = False
                st.session_state.historial_alertas.append({
                    **alerta,
                    'fecha_activacion': datetime.now(),
                    'precio_activacion': precio_actual
                })

            elif alerta['tipo'] == 'bajada' and precio_actual <= alerta['precio_objetivo']:
                alertas_activadas.append({
                    'ticker': alerta['ticker'],
                    'precio_actual': precio_actual,
                    'precio_objetivo': alerta['precio_objetivo'],
                    'tipo': 'bajada',
                    'comentario': alerta.get('comentario', '')
                })
                # Desactivar alerta y mover al historial
                st.session_state.alertas[i]['activa'] = False
                st.session_state.historial_alertas.append({
                    **alerta,
                    'fecha_activacion': datetime.now(),
                    'precio_activacion': precio_actual
                })

    return alertas_activadas

def eliminar_alerta(alerta_id):
    """Elimina una alerta del sistema"""
    st.session_state.alertas = [a for a in st.session_state.alertas if a.get('id') != alerta_id]

# SIDEBAR Y CONFIGURACIÓN
with st.sidebar:
    st.markdown("### 🎯 Configuración del Análisis")

    # Selector de mercado
    indice = st.selectbox(
        "📈 Selecciona el mercado:",
        ["S&P 500", "IBEX 35", "Mercados Asiáticos", "Criptomonedas"],
        help="Elige el mercado que quieres analizar"
    )

    # Información del mercado seleccionado
    info_mercados = {
        "S&P 500": "🇺🇸 Las 500 empresas más grandes de Estados Unidos",
        "IBEX 35": "🇪🇸 Las 35 empresas más líquidas de España",
        "Mercados Asiáticos": "🌏 Principales empresas de Asia-Pacífico",
        "Criptomonedas": "₿ Las principales criptomonedas del mercado"
    }
    st.info(info_mercados[indice])

    # Filtro de búsqueda
    filtro_busqueda = st.text_input(
        "🔍 Buscar acciones:",
        placeholder="Ej: AAPL, Apple, Microsoft, Banco...",
        help="Busca por ticker o nombre de empresa"
    )

    st.markdown("### ⚙️ Configuración de Datos")

    # Opción para usar API real
    usar_api_real = st.checkbox(
        "📡 Usar datos reales (API)",
        value=False,
        help="Activa para usar datos reales de Alpha Vantage (más lento)"
    )

    if usar_api_real:
        st.warning("⚠️ Los datos reales pueden tardar más en cargar debido a límites de API")

    # Opción para mostrar gráficos
    mostrar_graficos = st.checkbox(
        "📊 Mostrar gráficos",
        value=True,
        help="Mostrar gráficos de rendimiento y análisis"
    )

    # Número de acciones a mostrar
    num_acciones = st.slider(
        "📋 Número de acciones a mostrar:",
        min_value=10,
        max_value=50,
        value=20,
        help="Selecciona cuántas acciones mostrar en la tabla"
    )

    st.markdown("### 🎨 Configuración Visual")

    # Columnas avanzadas
    mostrar_columnas_avanzadas = st.checkbox(
        "📊 Mostrar columnas avanzadas",
        value=True,
        help="Incluir indicadores técnicos y fundamentales adicionales"
    )

    # Tema oscuro (experimental)
    tema_oscuro = st.checkbox(
        "🌙 Modo oscuro (experimental)",
        value=False,
        help="Cambiar a tema oscuro"
    )

    st.markdown("### 🚨 Sistema de Alertas")

    # Inicializar sistema de alertas
    inicializar_alertas()

    # Crear nueva alerta
    with st.expander("➕ Crear Nueva Alerta", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            ticker_alerta = st.text_input("Ticker:", placeholder="Ej: AAPL")
        with col2:
            tipo_alerta = st.selectbox("Tipo:", ["subida", "bajada"])

        precio_alerta = st.number_input(
            "Precio objetivo:",
            min_value=0.000001,
            step=0.01,
            format="%.6f"
        )

        comentario_alerta = st.text_area(
            "Comentario (opcional):",
            placeholder="Ej: Comprar si rompe resistencia...",
            max_chars=100
        )

        if st.button("🔔 Crear Alerta", type="primary"):
            if ticker_alerta and precio_alerta > 0:
                agregar_alerta(ticker_alerta.upper(), precio_alerta, tipo_alerta, comentario_alerta)
                st.success(f"✅ Alerta creada para {ticker_alerta.upper()}")
                st.rerun()
            else:
                st.error("❌ Por favor completa todos los campos obligatorios")

    # Mostrar alertas activas
    alertas_activas = [a for a in st.session_state.alertas if a['activa']]
    if alertas_activas:
        st.markdown("#### 🔔 Alertas Activas:")
        for alerta in alertas_activas:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    emoji = "📈" if alerta['tipo'] == 'subida' else "📉"
                    st.write(f"{emoji} **{alerta['ticker']}**: ${alerta['precio_objetivo']:.6f}")
                    if alerta.get('comentario'):
                        st.caption(alerta['comentario'])
                with col2:
                    if st.button("🗑️", key=f"del_{alerta['id']}", help="Eliminar alerta"):
                        eliminar_alerta(alerta['id'])
                        st.rerun()
    else:
        st.info("📝 No tienes alertas activas")

    # Historial de alertas
    if st.session_state.historial_alertas:
        with st.expander("📜 Historial de Alertas"):
            for alerta in st.session_state.historial_alertas[-5:]:  # Últimas 5
                emoji = "🚀" if alerta['tipo'] == 'subida' else "📉"
                st.write(f"{emoji} {alerta['ticker']} - ${alerta['precio_activacion']:.2f}")
                st.caption(f"Activada: {alerta['fecha_activacion'].strftime('%d/%m %H:%M')}")

    st.markdown("---")
    st.markdown("### ℹ️ Información")
    st.info(
        """
        **💡 Consejos:**
        - Verde: Oportunidades de compra
        - Amarillo: Mantener posición
        - Rojo: Considerar venta
        - RSI < 30: Posible sobreventa
        - RSI > 70: Posible sobrecompra
        """
    )

# CONTENIDO PRINCIPAL
st.markdown("### 📊 Panel de Análisis Avanzado de Acciones")

# Obtener datos
tickers = obtener_tickers(indice)
df = obtener_datos_acciones(tickers[:num_acciones], filtro_busqueda, usar_api_real)

# Mostrar alertas activadas
alertas_activadas = verificar_alertas(df)
if alertas_activadas:
    for alerta in alertas_activadas:
        tipo = "⬆️" if alerta['tipo'] == 'subida' else "⬇️"
        st.markdown(
            f"""
            <div class="alert-card success-alert">
                <b>{tipo} ¡Alerta activada para {alerta['ticker']}!</b><br>
                Precio actual: <b>${alerta['precio_actual']:.2f}</b> | Objetivo: <b>${alerta['precio_objetivo']:.2f}</b><br>
                {alerta['comentario']}
            </div>
            """, unsafe_allow_html=True
        )

# Mostrar tabla de resultados
if not df.empty:
    st.markdown("#### 📋 Resultados del análisis")
    st.write(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
else:
    st.warning("No se encontraron acciones para mostrar con los filtros seleccionados.")

# Mostrar métricas agregadas
if not df.empty:
    st.markdown("#### 📈 Métricas agregadas")
    col1, col2, col3 = st.columns(3)

    # Calcular ganancia media
    try:
        ganancia_media = np.mean([
            float(re.search(r'([-+]?\d*\.?\d+)', row['Ganancia Potencial']).group(1))
            for _, row in df.iterrows()
        ])
    except Exception:
        ganancia_media = 0

    # Contar recomendaciones
    num_compra = sum('COMPRA' in row['Recomendación'] for _, row in df.iterrows())
    num_venta = sum('VENDER' in row['Recomendación'] for _, row in df.iterrows())
    num_mantener = sum('MANTENER' in row['Recomendación'] for _, row in df.iterrows())

    col1.metric("Ganancia Potencial Media", f"{ganancia_media:.1f}%")
    col2.metric("Oportunidades de Compra", num_compra)
    col3.metric("Recomendaciones de Venta", num_venta)

    st.caption(f"Acciones en mantener: {num_mantener}")

# Mostrar gráficos si está activado
if not df.empty and mostrar_graficos:
    st.markdown("#### 📊 Gráficos de análisis")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = crear_grafico_rendimiento(df)
        if fig1:
            st.pyplot(fig1)

    with col2:
        fig2 = crear_grafico_sectorial(df)
        if fig2:
            st.pyplot(fig2)

# FOOTER Y DISCLAIMER LEGAL
st.markdown(
    """
    <div class="footer-container">
        <b>Oráculo de Omaha</b> no está afiliado a Warren Buffett ni a Berkshire Hathaway.<br>
        Esta aplicación es solo para fines educativos y de entretenimiento.<br>
        <b>No constituye asesoramiento financiero.</b> Consulta siempre con un profesional antes de invertir.<br>
        <br>
        <span style="font-size:1.1rem;">Desarrollado con ❤️ por la comunidad inversora.</span>
    </div>
    """,
    unsafe_allow_html=True
)
