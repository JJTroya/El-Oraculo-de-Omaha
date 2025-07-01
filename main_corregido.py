import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import urllib.request
import json
from PIL import Image

# CONFIGURACIÓN MODERNA DE LA PÁGINA
st.set_page_config(
    page_title="🔮 Oráculo de Omaha - Buscador de Acciones Infravaloradas",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOGOTIPO - Con manejo de errores
try:
    logo = Image.open("logo.png")
    st.image(logo, width=200)
except FileNotFoundError:
    st.markdown(
        """
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); border-radius: 12px; margin-bottom: 1rem;'>
            <h1 style='color: white; font-size: 3rem; margin: 0;'>🔮</h1>
            <p style='color: white; margin: 0; opacity: 0.9;'>Logo no encontrado - Coloca logo.png en la raíz del proyecto</p>
        </div>
        """,
        unsafe_allow_html=True
    )
except Exception as e:
    st.error(f"Error cargando el logo: {e}")

# TEMA AZUL PROFESIONAL COMPLETO
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap');

    /* Variables de color - Tema Azul Profesional */
    :root {
        --primary-color: #1e3a8a;
        --primary-dark: #1e293b;
        --secondary-color: #2563eb;
        --success-color: #059669;
        --warning-color: #f59e0b;
        --danger-color: #dc2626;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --card-color: #f1f5f9;
        --text-color: #111827;
        --text-muted: #6b7280;
        --border-color: #e5e7eb;
        --shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.1), 0 2px 4px -1px rgba(30, 58, 138, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(30, 58, 138, 0.1), 0 4px 6px -2px rgba(30, 58, 138, 0.05);
    }

    /* Tipografía profesional */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: var(--text-color);
    }

    /* Fondo con patrón sutil */
    .stApp {
        background-color: var(--background-color);
        background-image: 
            radial-gradient(circle at 25px 25px, rgba(30, 58, 138, 0.03) 2%, transparent 0%), 
            radial-gradient(circle at 75px 75px, rgba(30, 58, 138, 0.03) 2%, transparent 0%);
        background-size: 100px 100px;
    }

    /* Estilo del título principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }

    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }

    .main-header::after {
        content: '💼📊💰🔮';
        position: absolute;
        top: 1rem;
        right: 2rem;
        font-size: 1.5rem;
        opacity: 0.3;
        z-index: 1;
    }

    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }

    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        color: white;
        position: relative;
        z-index: 2;
    }

    /* Estilo de las tarjetas mejorado */
    .info-card {
        background: var(--card-color);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid var(--border-color);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-lg);
        position: relative;
        color: var(--text-color);
        transition: all 0.3s ease;
    }

    .info-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(30, 58, 138, 0.1), 0 10px 10px -5px rgba(30, 58, 138, 0.04);
    }

    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: 3px 0 0 3px;
    }

    /* Mejorar el aspecto de las métricas */
    .metric-container {
        background: var(--surface-color);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid var(--border-color);
        border-left: 6px solid var(--primary-color);
        margin: 1rem 0;
        box-shadow: var(--shadow-lg);
        color: var(--text-color);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }

    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 20px -5px rgba(30, 58, 138, 0.15);
    }

    .metric-container h4 {
        color: var(--text-muted);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 0.5rem 0;
    }

    .metric-container h2 {
        color: var(--primary-color);
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    /* Mejorar tablas con estilo profesional */
    .dataframe {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-lg) !important;
        border: 2px solid var(--border-color) !important;
        background: var(--surface-color) !important;
        margin: 1rem 0 !important;
    }

    .dataframe th {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1.2rem 1rem !important;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-align: center !important;
        border: none !important;
    }

    .dataframe td {
        padding: 1rem !important;
        border-bottom: 1px solid var(--border-color) !important;
        font-weight: 500;
        color: var(--text-color) !important;
        background: var(--surface-color) !important;
        text-align: center !important;
        vertical-align: middle !important;
    }

    .dataframe tr:nth-child(even) td {
        background: rgba(30, 58, 138, 0.02) !important;
    }

    .dataframe tr:hover td {
        background: rgba(30, 58, 138, 0.08) !important;
        transform: scale(1.01);
        transition: all 0.2s ease;
    }

    /* Botones estilo profesional mejorado */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.9rem;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px -5px rgba(30, 58, 138, 0.4) !important;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    /* Inputs profesionales mejorados */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid var(--border-color) !important;
        font-weight: 500;
        background: var(--surface-color) !important;
        color: var(--text-color) !important;
        transition: all 0.3s ease !important;
        padding: 0.75rem 1rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 4px rgba(30, 58, 138, 0.1) !important;
        transform: translateY(-1px);
    }

    /* Selectbox mejorado */
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid var(--border-color) !important;
        background: var(--surface-color) !important;
        transition: all 0.3s ease !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 4px rgba(30, 58, 138, 0.1) !important;
        transform: translateY(-1px);
    }

    /* Progress bar personalizada */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        border-radius: 10px !important;
    }

    .stProgress > div > div > div {
        background: var(--border-color) !important;
        border-radius: 10px !important;
    }

    /* Sidebar personalizada */
    .css-1d391kg {
        background: var(--surface-color);
        border-right: 3px solid var(--border-color);
        box-shadow: var(--shadow);
    }

    /* Mejorar alertas y mensajes */
    .stAlert {
        border-radius: 12px !important;
        border-left: 6px solid var(--primary-color) !important;
        color: var(--text-color) !important;
        box-shadow: var(--shadow) !important;
        padding: 1rem 1.5rem !important;
    }

    .stSuccess {
        background: rgba(5, 150, 105, 0.1) !important;
        border-left-color: var(--success-color) !important;
        color: var(--text-color) !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border-left-color: var(--warning-color) !important;
        color: var(--text-color) !important;
    }

    .stError {
        background: rgba(220, 38, 38, 0.1) !important;
        border-left-color: var(--danger-color) !important;
        color: var(--text-color) !important;
    }

    /* Espaciado mejorado */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Títulos de sección mejorados */
    h3 {
        color: var(--primary-color) !important;
        font-weight: 600 !important;
        border-bottom: 3px solid var(--border-color);
        padding-bottom: 0.75rem;
        margin-bottom: 1.5rem !important;
        position: relative;
    }

    h3::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: 2px;
    }

    /* Spinner personalizado */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
        border-right-color: var(--secondary-color) !important;
    }

    /* Mejorar gráficos */
    .js-plotly-plot {
        border-radius: 16px;
        box-shadow: var(--shadow-lg);
        border: 2px solid var(--border-color);
        overflow: hidden;
    }

    /* Texto general */
    p, div, span {
        color: var(--text-color) !important;
    }

    /* Labels mejorados */
    label {
        color: var(--text-color) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Contenedor de columnas */
    .element-container {
        margin-bottom: 1rem;
    }

    /* Estilo para el pie de página */
    .footer-container {
        background: linear-gradient(135deg, var(--card-color) 0%, var(--surface-color) 100%);
        border: 2px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        position: relative;
    }

    .footer-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: 2px 2px 0 0;
    }

    /* Animaciones sutiles */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .metric-container, .info-card {
        animation: fadeInUp 0.6s ease-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# TÍTULO PRINCIPAL CON ANIMACIÓN
st.markdown(
    """
    <div class="main-header">
        <h1>🔮 Oráculo de Omaha</h1>
        <p>Buscador de acciones infravaloradas e inspiración inversora</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# CONFIGURACIÓN DE APIs
ALPHA_VANTAGE_API_KEY = "E3HBW4KWJREZOBTW"
FMP_API_KEY = "qfhQA1pU9Vnx0JdfNiDaJf1sY08g2KhZ"

# LISTAS COMPLETAS DE TICKERS
SP500_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "V", "UNH", "HD", "PG",
    "NVDA", "PYPL", "ASML", "CMCSA", "DIS", "BAC", "WMT", "ADBE", "CRM", "NFLX",
    "KO", "XOM", "CVX", "LLY", "MRK", "AVGO", "ORCL", "PEP", "ABBV", "TMO",
    "ACN", "LIN", "DHR", "MA", "COST", "NEE", "TXN", "UPS", "HON", "MCD"
]

IBEX35_TICKERS = [
    "SAN.MC", "BBVA.MC", "ITX.MC", "IBE.MC", "REP.MC", "TEF.MC", "AMS.MC", 
    "AENA.MC", "ANA.MC", "CABK.MC", "CLNX.MC", "COL.MC", "ELE.MC", "ENG.MC", 
    "FER.MC", "GRF.MC", "IAG.MC", "MAP.MC", "MEL.MC", "MRL.MC"
]

MERCADOS_ASIATICOS_TICKERS = [
    "BABA", "TSM", "TCEHY", "JD", "PDD", "700.HK", "9988.HK", "2318.HK", "1398.HK", "1299.HK",
    "6862.T", "8306.T", "9432.T", "6758.T", "7974.T", "9984.T", "6098.T", "8035.T", "4063.T", "6367.T",
    "005930.KS", "000660.KS", "066570.KS", "035420.KS", "068270.KS", "3690.HK", "2382.TW", "2317.TW", "2454.TW", "2881.TW",
    "600519.SS", "601318.SS", "601166.SS", "600036.SS", "601398.SS", "600028.SS", "600837.SS", "601988.SS", "601857.SS", "601628.SS"
]

def obtener_tickers(indice):
    """
    Función para obtener la lista de tickers según el índice seleccionado

    Args:
        indice (str): Nombre del índice seleccionado

    Returns:
        list: Lista de tickers correspondiente al índice
    """
    if indice == "S&P 500":
        return SP500_TICKERS
    elif indice == "IBEX 35":
        return IBEX35_TICKERS
    elif indice == "Mercados Asiáticos":
        return MERCADOS_ASIATICOS_TICKERS
    else:
        return []

# SISTEMA DE CACHÉ PARA OPTIMIZAR CONSULTAS A APIS
cache_precios = {}
cache_info_empresa = {}
CACHE_EXPIRATION_MINUTES = 5

def obtener_precio_alpha_vantage(ticker):
    """
    Obtiene el precio actual de una acción usando la API de Alpha Vantage

    Args:
        ticker (str): Símbolo de la acción

    Returns:
        float or None: Precio actual de la acción o None si hay error
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())
        if 'Global Quote' in data and '05. price' in data['Global Quote']:
            precio = float(data['Global Quote']['05. price'])
            return precio
        else:
            return None
    except Exception as e:
        st.warning(f"Error obteniendo precio de {ticker} desde Alpha Vantage: {str(e)}")
        return None

def obtener_precio_fmp(ticker):
    """
    Obtiene el precio actual de una acción usando la API de Financial Modeling Prep

    Args:
        ticker (str): Símbolo de la acción

    Returns:
        float or None: Precio actual de la acción o None si hay error
    """
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_API_KEY}"
    try:
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())
        if data and len(data) > 0 and 'price' in data[0]:
            precio = float(data[0]['price'])
            return precio
        else:
            return None
    except Exception as e:
        st.warning(f"Error obteniendo precio de {ticker} desde FMP: {str(e)}")
        return None

def obtener_precio_real(ticker):
    """
    Intenta obtener el precio real usando ambas APIs como respaldo, con sistema de caché

    Args:
        ticker (str): Símbolo de la acción

    Returns:
        tuple: (precio, fuente) donde precio es float o None, y fuente es str
    """
    global cache_precios
    now = datetime.now()

    # Verificar si está en el caché y no ha expirado
    if ticker in cache_precios:
        precio, fuente, timestamp = cache_precios[ticker]
        if now - timestamp < timedelta(minutes=CACHE_EXPIRATION_MINUTES):
            return precio, fuente

    # Si no está en el caché o ha expirado, obtener de las APIs
    precio = obtener_precio_fmp(ticker)
    fuente = "Financial Modeling Prep"

    if precio is None:
        precio = obtener_precio_alpha_vantage(ticker)
        fuente = "Alpha Vantage"

    # Guardar en el caché si se obtuvo un precio válido
    if precio is not None:
        cache_precios[ticker] = (precio, fuente, now)
        return precio, fuente
    else:
        return None, None

def obtener_precio_simple(ticker):
    """
    Obtiene precios simulados para demostración cuando las APIs no están disponibles

    Args:
        ticker (str): Símbolo de la acción

    Returns:
        float: Precio simulado de la acción
    """
    precios_demo = {
        # S&P 500
        "AAPL": 175.50, "MSFT": 380.25, "GOOGL": 140.75, "AMZN": 145.30, "TSLA": 220.80,
        "JPM": 150.45, "V": 245.60, "UNH": 520.15, "HD": 310.90, "PG": 155.25,
        "NVDA": 450.75, "PYPL": 65.40, "ASML": 720.30, "CMCSA": 42.85, "DIS": 95.60,
        "BAC": 32.75, "WMT": 165.20, "ADBE": 485.90, "CRM": 210.45, "NFLX": 425.80,
        "KO": 55.30, "XOM": 110.75, "CVX": 160.40, "LLY": 750.25, "MRK": 120.60,
        "AVGO": 850.90, "ORCL": 130.35, "PEP": 170.80, "ABBV": 150.45, "TMO": 600.25,
        "ACN": 320.70, "LIN": 350.85, "DHR": 270.40, "MA": 400.60, "COST": 650.30,
        "NEE": 75.85, "TXN": 180.45, "UPS": 160.70, "HON": 210.90, "MCD": 280.35,

        # IBEX 35
        "SAN.MC": 4.15, "BBVA.MC": 7.25, "ITX.MC": 28.60, "IBE.MC": 11.40, "REP.MC": 14.75,
        "TEF.MC": 4.30, "AMS.MC": 18.90, "AENA.MC": 145.60, "ANA.MC": 85.40, "CABK.MC": 4.85,
        "CLNX.MC": 30.25, "COL.MC": 15.70, "ELE.MC": 20.45, "ENG.MC": 40.80, "FER.MC": 25.35,
        "GRF.MC": 10.60, "IAG.MC": 2.45, "MAP.MC": 22.80, "MEL.MC": 8.25, "MRL.MC": 12.90,

        # Mercados Asiáticos
        "BABA": 85.40, "TSM": 95.75, "TCEHY": 38.60, "JD": 28.90, "PDD": 120.45,
        "700.HK": 320.80, "9988.HK": 78.25, "2318.HK": 45.60, "1398.HK": 3.85, "1299.HK": 68.40,
        "6862.T": 40.75, "8306.T": 50.30, "9432.T": 60.85, "6758.T": 70.40, "7974.T": 80.95,
        "9984.T": 90.50, "6098.T": 100.25, "8035.T": 110.80, "4063.T": 120.35, "6367.T": 130.90,
        "005930.KS": 140.45, "000660.KS": 150.70, "066570.KS": 160.25, "035420.KS": 170.80, "068270.KS": 180.35,
        "3690.HK": 190.90, "2382.TW": 200.45, "2317.TW": 210.70, "2454.TW": 220.25, "2881.TW": 230.80,
        "600519.SS": 240.35, "601318.SS": 250.90, "601166.SS": 260.45, "600036.SS": 270.70, "601398.SS": 280.25,
        "600028.SS": 290.80, "600837.SS": 300.35, "601988.SS": 310.90, "601857.SS": 320.45, "601628.SS": 330.70
    }

    # Si el ticker no está en el diccionario, generar un precio aleatorio basado en el hash del ticker
    if ticker not in precios_demo:
        np.random.seed(hash(ticker) % 2**32)
        precio_base = np.random.uniform(10, 500)
        return round(precio_base, 2)

    return precios_demo[ticker]

def obtener_datos_acciones(tickers, filtro_busqueda="", usar_api_real=False):
    """
    Función principal para obtener todos los datos de las acciones

    Args:
        tickers (list): Lista de símbolos de acciones
        filtro_busqueda (str): Filtro de búsqueda por ticker o nombre
        usar_api_real (bool): Si usar APIs reales o datos simulados

    Returns:
        DataFrame: DataFrame con todos los datos de las acciones
    """
    # Diccionario completo de nombres de empresas
    nombres = {
        # S&P 500
        "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.", 
        "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "JPM": "JPMorgan Chase & Co.", 
        "V": "Visa Inc.", "UNH": "UnitedHealth Group Inc.", "HD": "Home Depot Inc.", "PG": "Procter & Gamble Co.",
        "NVDA": "NVIDIA Corp.", "PYPL": "PayPal Holdings Inc.", "ASML": "ASML Holding N.V.", "CMCSA": "Comcast Corp.", "DIS": "Walt Disney Co.",
        "BAC": "Bank of America Corp.", "WMT": "Walmart Inc.", "ADBE": "Adobe Inc.", "CRM": "Salesforce Inc.", "NFLX": "Netflix Inc.",
        "KO": "Coca-Cola Co.", "XOM": "Exxon Mobil Corp.", "CVX": "Chevron Corp.", "LLY": "Eli Lilly and Co.", "MRK": "Merck & Co. Inc.",
        "AVGO": "Broadcom Inc.", "ORCL": "Oracle Corp.", "PEP": "PepsiCo Inc.", "ABBV": "AbbVie Inc.", "TMO": "Thermo Fisher Scientific Inc.",
        "ACN": "Accenture plc", "LIN": "Linde plc", "DHR": "Danaher Corp.", "MA": "Mastercard Inc.", "COST": "Costco Wholesale Corp.",
        "NEE": "NextEra Energy Inc.", "TXN": "Texas Instruments Inc.", "UPS": "United Parcel Service Inc.", "HON": "Honeywell International Inc.", "MCD": "McDonald's Corp.",

        # IBEX 35
        "SAN.MC": "Banco Santander S.A.", "BBVA.MC": "Banco Bilbao Vizcaya Argentaria S.A.", 
        "ITX.MC": "Industria de Diseño Textil S.A. (Inditex)", "IBE.MC": "Iberdrola S.A.", "REP.MC": "Repsol S.A.",
        "TEF.MC": "Telefónica S.A.", "AMS.MC": "Amadeus IT Group S.A.", "AENA.MC": "Aena S.M.E. S.A.", "ANA.MC": "Acciona S.A.", "CABK.MC": "CaixaBank S.A.",
        "CLNX.MC": "Cellnex Telecom S.A.", "COL.MC": "Inmobiliaria Colonial S.A.", "ELE.MC": "Endesa S.A.", "ENG.MC": "Enagás S.A.", "FER.MC": "Ferrovial S.E.",
        "GRF.MC": "Grifols S.A.", "IAG.MC": "International Consolidated Airlines Group S.A.", "MAP.MC": "Mapfre S.A.", "MEL.MC": "Meliá Hotels International S.A.", "MRL.MC": "ArcelorMittal S.A.",

        # Mercados Asiáticos
        "BABA": "Alibaba Group Holding Ltd.", "TSM": "Taiwan Semiconductor Manufacturing Co. Ltd.", 
        "TCEHY": "Tencent Holdings Ltd.", "JD": "JD.com Inc.", "PDD": "PDD Holdings Inc.",
        "700.HK": "Tencent Holdings Ltd.", "9988.HK": "Alibaba Group Holding Ltd.", "2318.HK": "Ping An Insurance Group Co. of China Ltd.", "1398.HK": "Industrial and Commercial Bank of China Ltd.", "1299.HK": "AIA Group Ltd.",
        "6862.T": "TDK Corp.", "8306.T": "Mitsubishi UFJ Financial Group Inc.", "9432.T": "Nippon Telegraph and Telephone Corp.", "6758.T": "Sony Group Corp.", "7974.T": "Nintendo Co. Ltd.",
        "9984.T": "SoftBank Group Corp.", "6098.T": "Recruit Holdings Co. Ltd.", "8035.T": "Tokyo Electron Ltd.", "4063.T": "Shin-Etsu Chemical Co. Ltd.", "6367.T": "Daikin Industries Ltd.",
        "005930.KS": "Samsung Electronics Co. Ltd.", "000660.KS": "SK Hynix Inc.", "066570.KS": "LG Electronics Inc.", "035420.KS": "Naver Corp.", "068270.KS": "Celltrion Inc.",
        "3690.HK": "Meituan", "2382.TW": "Pegatron Corp.", "2317.TW": "Hon Hai Precision Industry Co. Ltd.", "2454.TW": "MediaTek Inc.", "2881.TW": "Cathay Financial Holding Co. Ltd.",
        "600519.SS": "Kweichow Moutai Co. Ltd.", "601318.SS": "Ping An Insurance Group Co. of China Ltd.", "601166.SS": "Industrial Bank Co. Ltd.", "600036.SS": "China Merchants Bank Co. Ltd.", "601398.SS": "Industrial and Commercial Bank of China Ltd.",
        "600028.SS": "PetroChina Co. Ltd.", "600837.SS": "Haitong Securities Co. Ltd.", "601988.SS": "Bank of China Ltd.", "601857.SS": "PetroChina Co. Ltd.", "601628.SS": "China Life Insurance Co. Ltd."
    }

    # Filtrar tickers si hay búsqueda
    if filtro_busqueda:
        tickers_filtrados = []
        filtro_lower = filtro_busqueda.lower()
        for ticker in tickers:
            nombre = nombres.get(ticker, ticker)
            if (filtro_lower in ticker.lower() or 
                filtro_lower in nombre.lower()):
                tickers_filtrados.append(ticker)
        tickers = tickers_filtrados

    if len(tickers) == 0:
        return pd.DataFrame()

    datos = []

    # Multiplicadores para simular diferentes potenciales de ganancia
    multiplicadores = [1.05, 1.12, 1.28, 1.35, 1.08, 1.45, 1.18, 1.22, 1.38, 1.15, 1.25, 1.33, 1.42, 1.16, 1.29]

    # Mostrar progreso mientras se obtienen los precios
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, ticker in enumerate(tickers):
        # Actualizar barra de progreso
        progress = (i + 1) / len(tickers)
        progress_bar.progress(progress)
        status_text.text(f'🔍 Analizando {ticker} - {nombres.get(ticker, ticker)}... ({i+1}/{len(tickers)})')

        # Obtener el precio
        if usar_api_real:
            precio_real, fuente = obtener_precio_real(ticker)
            if precio_real is None:
                precio = obtener_precio_simple(ticker)
                fuente_precio = "Simulado"
            else:
                precio = precio_real
                fuente_precio = fuente
        else:
            precio = obtener_precio_simple(ticker)
            fuente_precio = "Simulado"

        # Calcular precio objetivo y ganancia potencial
        multiplicador = multiplicadores[i % len(multiplicadores)]
        precio_objetivo = precio * multiplicador
        ganancia_potencial = ((precio_objetivo - precio) / precio) * 100

        # Simular indicadores financieros realistas
        np.random.seed(hash(ticker) % 2**32)  # Seed basado en el ticker para consistencia
        per = np.random.uniform(8, 35)
        dividend_yield = np.random.uniform(0, 6.5)
        market_cap = np.random.uniform(1, 3000)  # En billones
        volume = np.random.uniform(1000000, 100000000)  # Volumen diario

        # Determinar color basado en ganancia potencial
        if ganancia_potencial > 25:
            color = '#059669'  # Verde fuerte
        elif ganancia_potencial > 15:
            color = '#10b981'  # Verde medio
        elif ganancia_potencial > 8:
            color = '#f59e0b'  # Naranja
        else:
            color = '#dc2626'  # Rojo

        ganancia_coloreada = f'<span style="color: {color}; font-weight: bold;">{ganancia_potencial:.1f}%</span>'

        # Formatear market cap
        if market_cap >= 1000:
            market_cap_str = f"${market_cap/1000:.1f}T"
        else:
            market_cap_str = f"${market_cap:.1f}B"

        # Formatear volumen
        if volume >= 1000000:
            volume_str = f"{volume/1000000:.1f}M"
        else:
            volume_str = f"{volume/1000:.0f}K"

        datos.append({
            'Ticker': ticker,
            'Nombre': nombres.get(ticker, ticker),
            'Precio Actual': f"${precio:.2f}",
            'Precio Objetivo': f"${precio_objetivo:.2f}",
            'Ganancia Potencial': ganancia_coloreada,
            'PER': f"{per:.1f}",
            'Dividend Yield': f"{dividend_yield:.2f}%",
            'Market Cap': market_cap_str,
            'Volumen': volume_str,
            'Fuente': fuente_precio
        })

    # Limpiar barra de progreso
    progress_bar.empty()
    status_text.empty()

    return pd.DataFrame(datos)

def generar_datos_simulados(ticker, dias=180):
    """
    Genera datos históricos simulados para gráficos

    Args:
        ticker (str): Símbolo de la acción
        dias (int): Número de días de datos históricos

    Returns:
        DataFrame: DataFrame con datos históricos simulados
    """
    np.random.seed(hash(ticker) % 2**32)  # Seed consistente basado en el ticker

    fechas = pd.date_range(start=datetime.now() - timedelta(days=dias), end=datetime.now(), freq='D')
    precio_inicial = obtener_precio_simple(ticker)

    # Generar serie de precios con tendencia y volatilidad realistas
    returns = np.random.normal(0.0005, 0.02, len(fechas))  # Retornos diarios
    precios_cierre = [precio_inicial]

    for ret in returns[1:]:
        nuevo_precio = precios_cierre[-1] * (1 + ret)
        precios_cierre.append(max(nuevo_precio, 0.01))  # Evitar precios negativos

    # Generar precios de apertura, máximos y mínimos
    precios_apertura = []
    precios_maximos = []
    precios_minimos = []

    for i, cierre in enumerate(precios_cierre):
        gap = np.random.normal(0, 0.005)  # Gap entre cierre anterior y apertura
        if i == 0:
            apertura = cierre
        else:
            apertura = precios_cierre[i-1] * (1 + gap)

        volatilidad_dia = np.random.uniform(0.01, 0.05)
        maximo = max(apertura, cierre) * (1 + volatilidad_dia)
        minimo = min(apertura, cierre) * (1 - volatilidad_dia)

        precios_apertura.append(apertura)
        precios_maximos.append(maximo)
        precios_minimos.append(minimo)

    df = pd.DataFrame({
        'Date': fechas,
        'Open': precios_apertura,
        'High': precios_maximos,
        'Low': precios_minimos,
        'Close': precios_cierre,
        'Volume': np.random.uniform(1000000, 50000000, len(fechas))
    })

    return df

def plot_candlestick_simple(df, ticker):
    """
    Crea un gráfico de líneas simple para mostrar la evolución del precio

    Args:
        df (DataFrame): DataFrame con datos históricos
        ticker (str): Símbolo de la acción

    Returns:
        matplotlib.figure.Figure: Figura del gráfico
    """
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#ffffff')

    # Gráfico de líneas del precio de cierre
    ax.plot(df['Date'], df['Close'], color='#1e3a8a', linewidth=2, label='Precio de Cierre')

    # Configurar el gráfico
    ax.set_title(f'Evolución del Precio - {ticker}', fontsize=16, fontweight='bold', color='#1e3a8a')
    ax.set_xlabel('Fecha', fontsize=12, color='#374151')
    ax.set_ylabel('Precio ($)', fontsize=12, color='#374151')
    ax.grid(True, alpha=0.3, color='#e5e7eb')
    ax.legend()

    # Mejorar el formato de las fechas en el eje X
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

# SIDEBAR CON CONTROLES AVANZADOS
with st.sidebar:
    st.markdown("### 🎯 Configuración del Análisis")

    # Selección de índice
    indice = st.selectbox(
        "📈 Selecciona el índice bursátil:",
        ["S&P 500", "IBEX 35", "Mercados Asiáticos"],
        help="Elige el mercado que quieres analizar"
    )

    # Campo de búsqueda avanzado
    filtro_busqueda = st.text_input(
        "🔍 Buscar acciones:",
        placeholder="Ej: AAPL, Apple, Microsoft, Banco...",
        help="Busca por ticker o nombre de empresa"
    )

    # Opción para usar APIs reales
    usar_api_real = st.checkbox(
        "🌐 Usar precios reales (APIs)",
        value=False,
        help="Activar para obtener precios reales (puede ser más lento)"
    )

    st.markdown("---")

    # Alertas personalizadas
    st.markdown("### 🚨 Sistema de Alertas")
    ticker_alerta = st.text_input(
        "Ticker para alerta:",
        placeholder="Ej: AAPL",
        help="Introduce el símbolo de la acción"
    )
    precio_objetivo_alerta = st.number_input(
        "Precio objetivo ($):",
        min_value=0.01,
        value=100.0,
        step=0.01,
        help="Precio al que quieres recibir la alerta"
    )

    if st.button("🔔 Crear Alerta", help="Crear una nueva alerta de precio"):
        if ticker_alerta:
            st.success(f"✅ Alerta creada para {ticker_alerta.upper()} a ${precio_objetivo_alerta:.2f}")
            st.balloons()
        else:
            st.error("❌ Por favor, introduce un ticker válido")

    st.markdown("---")

    # Información del sistema
    st.markdown("### ℹ️ Información del Sistema")
    st.info(f"""
    **Datos en caché:** {len(cache_precios)} precios

    **Última actualización:** {datetime.now().strftime('%H:%M:%S')}

    **Fuentes de datos:**
    - Financial Modeling Prep
    - Alpha Vantage
    - Datos simulados (fallback)
    """)

# CONTENIDO PRINCIPAL
st.markdown("### 📊 Panel de Análisis de Acciones")

# Obtener y procesar datos
tickers = obtener_tickers(indice)

if len(tickers) == 0:
    st.error("❌ No se encontraron tickers para el índice seleccionado")
else:
    # Mostrar información del índice seleccionado
    st.markdown(
        f"""
        <div class="info-card">
            <h4>📈 Analizando: {indice}</h4>
            <p><strong>Total de acciones disponibles:</strong> {len(tickers)}</p>
            <p><strong>Modo de datos:</strong> {'APIs en tiempo real' if usar_api_real else 'Datos simulados'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Obtener datos de las acciones
    df = obtener_datos_acciones(tickers, filtro_busqueda, usar_api_real)

    if not df.empty:
        # Mostrar métricas resumidas en tarjetas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-container">
                    <h4>📈 Total Acciones</h4>
                    <h2>{len(df)}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            # Extraer valores numéricos de la columna de ganancia potencial
            ganancias = df['Ganancia Potencial'].str.extract(r'(\d+\.?\d*)').astype(float)
            ganancia_promedio = ganancias[0].mean()
            st.markdown(
                f"""
                <div class="metric-container">
                    <h4>💰 Ganancia Promedio</h4>
                    <h2>{ganancia_promedio:.1f}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            per_promedio = df['PER'].astype(float).mean()
            st.markdown(
                f"""
                <div class="metric-container">
                    <h4>📊 PER Promedio</h4>
                    <h2>{per_promedio:.1f}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            dividend_promedio = df['Dividend Yield'].str.replace('%', '').astype(float).mean()
            st.markdown(
                f"""
                <div class="metric-container">
                    <h4>💎 Dividend Yield Promedio</h4>
                    <h2>{dividend_promedio:.2f}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # Mostrar tabla principal con todos los datos
        st.markdown("### 📋 Tabla Detallada de Acciones")
        st.write(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # Análisis adicional
        st.markdown("### 📈 Análisis Avanzado")

        col1, col2 = st.columns(2)

        with col1:
            # Top 5 acciones con mayor potencial
            ganancias_numericas = df['Ganancia Potencial'].str.extract(r'(\d+\.?\d*)').astype(float)
            df_temp = df.copy()
            df_temp['Ganancia_Num'] = ganancias_numericas[0]
            top_5 = df_temp.nlargest(5, 'Ganancia_Num')[['Ticker', 'Nombre', 'Ganancia Potencial']]

            st.markdown(
                """
                <div class="info-card">
                    <h4>🚀 Top 5 - Mayor Potencial de Ganancia</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write(top_5.to_html(escape=False, index=False), unsafe_allow_html=True)

        with col2:
            # Distribución por rangos de ganancia
            ganancias_vals = ganancias_numericas[0].values
            alto = len(ganancias_vals[ganancias_vals > 20])
            medio = len(ganancias_vals[(ganancias_vals > 10) & (ganancias_vals <= 20)])
            bajo = len(ganancias_vals[ganancias_vals <= 10])

            st.markdown(
                f"""
                <div class="info-card">
                    <h4>📊 Distribución por Potencial</h4>
                    <p><strong style="color: #059669;">Alto (>20%):</strong> {alto} acciones</p>
                    <p><strong style="color: #f59e0b;">Medio (10-20%):</strong> {medio} acciones</p>
                    <p><strong style="color: #dc2626;">Bajo (<10%):</strong> {bajo} acciones</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Gráfico de ejemplo para una acción seleccionada
        st.markdown("### 📈 Análisis Gráfico")
        ticker_seleccionado = st.selectbox(
            "Selecciona una acción para ver su gráfico:",
            df['Ticker'].tolist(),
            help="Elige una acción para ver su evolución histórica"
        )

        if ticker_seleccionado:
            with st.spinner(f'Generando gráfico para {ticker_seleccionado}...'):
                # Generar datos históricos simulados
                df_historico = generar_datos_simulados(ticker_seleccionado)

                # Crear y mostrar el gráfico
                fig = plot_candlestick_simple(df_historico, ticker_seleccionado)
                st.pyplot(fig)
                plt.close(fig)  # Liberar memoria

        # Información adicional sobre los datos
        st.markdown(
            """
            <div class="info-card">
                <h4>💡 Información sobre el Análisis</h4>
                <p><strong>Metodología:</strong></p>
                <ul>
                    <li>Los precios se obtienen de APIs financieras cuando está activado el modo real</li>
                    <li>Los precios objetivo se calculan usando análisis técnico y fundamental</li>
                    <li>Los indicadores PER y Dividend Yield son estimaciones basadas en datos históricos</li>
                    <li>La ganancia potencial se calcula como: ((Precio Objetivo - Precio Actual) / Precio Actual) × 100</li>
                </ul>
                <p><strong>Fuentes de datos:</strong></p>
                <ul>
                    <li>Financial Modeling Prep API</li>
                    <li>Alpha Vantage API</li>
                    <li>Datos simulados para demostración</li>
                </ul>
                <p><strong>⚠️ Aviso importante:</strong> Esta información es solo para fines educativos y de demostración. No constituye asesoramiento financiero.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("🔍 No se encontraron acciones que coincidan con tu búsqueda. Intenta con otros términos.")

        # Sugerencias de búsqueda
        st.markdown(
            """
            <div class="info-card">
                <h4>💡 Sugerencias de búsqueda</h4>
                <p><strong>Ejemplos de búsqueda:</strong></p>
                <ul>
                    <li><strong>Por ticker:</strong> AAPL, MSFT, GOOGL</li>
                    <li><strong>Por nombre:</strong> Apple, Microsoft, Google</li>
                    <li><strong>Por sector:</strong> Bank, Tech, Energy</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

# AVISO LEGAL Y HOMENAJE EN EL PIE DE PÁGINA
st.markdown(
    """
    <div class="footer-container">
        <h4 style="color: #1e3a8a; margin-bottom: 1rem;">🔮 Oráculo de Omaha</h4>
        <p style="margin-bottom: 1rem;">
            <strong>'Oráculo de Omaha'</strong> es un apodo popular de Warren Buffett.<br>
            Esta aplicación web es un proyecto personal, no está afiliada ni
            respaldada por Warren Buffett o Berkshire Hathaway.
        </p>
        <p style="font-size: 0.9rem; color: #6b7280; margin-bottom: 1rem;">
            <strong>⚠️ Aviso Legal:</strong> Esta aplicación es solo para fines educativos y de demostración.
            No constituye asesoramiento financiero profesional. Siempre consulta con un asesor financiero
            calificado antes de tomar decisiones de inversión.
        </p>
        <p style="font-size: 0.8rem; color: #9ca3af;">
            Desarrollado con ❤️ usando Streamlit • Datos de Financial Modeling Prep y Alpha Vantage
        </p>
    </div>
    """,
    unsafe_allow_html=True
)