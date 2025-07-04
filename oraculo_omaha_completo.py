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
import uuid

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
def render_header():
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

# ESTILOS CSS
def render_styles():
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
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ... resto de estilos intactos ... */
        </style>
        """, unsafe_allow_html=True
    )

# CLAVES DE API
ALPHA_VANTAGE_API_KEY = "Z1VNLB6FJ0L0WSU0"

# LISTAS DE TICKERS
SP500_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "TSLA", "BRK-B", "UNH", "JNJ", "XOM",
    # ... resto de tickers ...
]
IBEX35_TICKERS = [
    "SAN.MC", "BBVA.MC", "ITX.MC", "IBE.MC", "REP.MC", "TEF.MC", # ...
]
MERCADOS_ASIATICOS_TICKERS = [
    "BABA", "JD", "PDD", "NTES", "BIDU", # ...
]
CRYPTO_TICKERS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", # ...
]

def obtener_tickers(indice):
    return {
        "S&P 500": SP500_TICKERS,
        "IBEX 35": IBEX35_TICKERS,
        "Mercados Asiáticos": MERCADOS_ASIATICOS_TICKERS,
        "Criptomonedas": CRYPTO_TICKERS
    }.get(indice, [])

# SISTEMA DE CACHÉ
cache_precios = {}
CACHE_EXPIRATION_MINUTES = 0.1

def limpiar_cache():
    now = datetime.now()
    for key, (_, ts) in list(cache_precios.items()):
        if (now - ts).total_seconds() > CACHE_EXPIRATION_MINUTES * 60:
            del cache_precios[key]

# FUNCIONES DE PRECIO

def obtener_precio_simple(ticker):
    precios_demo = {
        "AAPL": 175.50, "MSFT": 380.25, "GOOGL": 140.75, # ...
        "SAN.MC": 4.15, "BBVA.MC": 7.25, # ... valores para IBEX
        "BABA": 85.40, "JD": 28.90, # ... valores para Asia
        "BTC-USD": 43250.80, "ETH-USD": 2650.45, # ... valores crypto
    }
    if ticker in precios_demo:
        base_price = precios_demo[ticker]
        variation = np.random.uniform(-0.02, 0.02)
        return round(base_price * (1 + variation), 6 if base_price < 1 else 2)
    else:
        np.random.seed(hash(ticker) % 2**32)
        if ticker.endswith('-USD'):
            precio_base = np.random.uniform(0.01, 50000)
        elif ticker.endswith('.MC'):
            precio_base = np.random.uniform(1, 100)
        else:
            precio_base = np.random.uniform(20, 800)
        return round(precio_base, 6 if precio_base < 1 else 2)


def obtener_precio_alpha_vantage(ticker):
    try:
        if ticker in cache_precios:
            data, ts = cache_precios[ticker]
            if (datetime.now() - ts).total_seconds() < CACHE_EXPIRATION_MINUTES * 60:
                return data
        ticker_clean = re.sub(r'\.(MC|HK|T|KS|TW|SS|SZ)$', '', ticker)
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker_clean}&apikey={ALPHA_VANTAGE_API_KEY}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            d = json.loads(resp.read().decode())
        precio = float(d["Global Quote"]["05. price"])
        cache_precios[ticker] = (precio, datetime.now())
        return precio
    except Exception as e:
        st.warning(f"Error API para {ticker}: {e}")
        return obtener_precio_simple(ticker)

# INDICADORES TÉCNICOS

def calcular_indicadores_tecnicos(ticker, precio_actual):
    np.random.seed(hash(ticker) % 2**32)
    rsi = np.random.uniform(20, 80)
    macd = np.random.uniform(-2, 2)
    bb_upper = precio_actual * np.random.uniform(1.02, 1.08)
    bb_lower = precio_actual * np.random.uniform(0.92, 0.98)
    ma_20 = precio_actual * np.random.uniform(0.95, 1.05)
    ma_50 = precio_actual * np.random.uniform(0.90, 1.10)
    ma_200 = precio_actual * np.random.uniform(0.85, 1.15)
    volumen_relativo = np.random.uniform(0.5, 2.5)
    stoch_k = np.random.uniform(10, 90)
    stoch_d = np.random.uniform(10, 90)
    return {
        'RSI': round(rsi, 1), 'MACD': round(macd, 3),
        'BB_Upper': round(bb_upper, 2), 'BB_Lower': round(bb_lower, 2),
        'MA_20': round(ma_20, 2), 'MA_50': round(ma_50, 2), 'MA_200': round(ma_200, 2),
        'Volumen_Relativo': round(volumen_relativo, 2), 'Stoch_K': round(stoch_k, 1), 'Stoch_D': round(stoch_d, 1)
    }

# DATOS FUNDAMENTALES

def obtener_datos_fundamentales(ticker):
    np.random.seed(hash(ticker) % 2**32)
    if ticker in ["AAPL","MSFT","GOOGL","AMZN","TSLA"]:
        pe_ratio = np.random.uniform(15, 35)
    elif ticker.endswith('.MC'):
        pe_ratio = np.random.uniform(8, 20)
    elif ticker.endswith('-USD'):
        pe_ratio = None
    else:
        pe_ratio = np.random.uniform(10, 25)
    if ticker in ["KO","PG","JNJ","VZ","T"]:
        dividend_yield = np.random.uniform(2, 6)
    elif ticker.endswith('-USD'):
        dividend_yield = 0
    else:
        dividend_yield = np.random.uniform(0, 4)
    if ticker in ["AAPL","MSFT","GOOGL","AMZN"]:
        market_cap = np.random.uniform(1.5, 3.0)
    elif ticker.endswith('.MC'):
        market_cap = np.random.uniform(0.01, 0.1)
    elif ticker.endswith('-USD'):
        market_cap = np.random.uniform(0.001, 0.1)
    else:
        market_cap = np.random.uniform(0.1, 1.0)
    pb_ratio = np.random.uniform(0.8, 4.5) if not ticker.endswith('-USD') else None
    roe = np.random.uniform(5, 25) if not ticker.endswith('-USD') else None
    debt_to_equity = np.random.uniform(0.1, 2.0) if not ticker.endswith('-USD') else None
    eps = np.random.uniform(1, 15) if not ticker.endswith('-USD') else None
    revenue_growth = np.random.uniform(-5, 25)
    return {
        'PE_Ratio': round(pe_ratio,1) if pe_ratio else None,
        'Dividend_Yield': round(dividend_yield,2),
        'Market_Cap': round(market_cap,2),
        'PB_Ratio': round(pb_ratio,1) if pb_ratio else None,
        'ROE': round(roe,1) if roe else None,
        'Debt_to_Equity': round(debt_to_equity,2) if debt_to_equity else None,
        'EPS': round(eps,2) if eps else None,
        'Revenue_Growth': round(revenue_growth,1)
    }

# OBTENER Y PROCESAR DATOS DE ACCIONES

def obtener_datos_acciones(tickers, filtro_busqueda="", usar_api_real=False):
    if filtro_busqueda:
        tickers = [t for t in tickers if filtro_busqueda.lower() in t.lower()]
    if not tickers:
        return pd.DataFrame()
    limpiar_cache()
    datos = []
    multiplicadores_objetivo = [1.05,1.12,1.28,1.35,1.08,1.45,1.18,1.22,1.38,1.15]
    for i,ticker in enumerate(tickers[:50]):
        precio = obtener_precio_alpha_vantage(ticker) if usar_api_real else obtener_precio_simple(ticker)
        objetivo = precio * multiplicadores_objetivo[i % len(multiplicadores_objetivo)]
        ganancia = ((objetivo - precio)/precio)*100
        fund = obtener_datos_fundamentales(ticker)
        tec = calcular_indicadores_tecnicos(ticker, precio)
        simbolo = '€' if ticker.endswith('.MC') else '$'
        # Recomendaciones ajustadas
        if ganancia > 30:
            rec, color = '🚀 COMPRA FUERTE','#059669'
        elif ganancia > 20:
            rec, color = '📈 COMPRA','#10b981'
        elif ganancia > 10:
            rec, color = '📈 COMPRA','#10b981'
        elif ganancia > 0:
            rec, color = '⚖️ MANTENER','#f59e0b'
        else:
            rec, color = '📉 VENDER','#dc2626'
        datos.append({
            'Ticker': ticker,
            'Empresa': ticker,
            'Precio Actual': f"{simbolo}{precio:.2f}",
            'Precio Objetivo': f"{simbolo}{objetivo:.2f}",
            'Ganancia Potencial': f"{ganancia:.1f}%",
            'Recomendación': rec,
            'P/E Ratio': fund['PE_Ratio'] if fund['PE_Ratio'] else 'N/A',
            'Dividend Yield': f"{fund['Dividend_Yield']:.2f}%" if fund['Dividend_Yield']>0 else 'N/A',
            'RSI': tec['RSI'],
            'MA 20': tec['MA_20'],
            'MA 50': tec['MA_50'],
            'Market Cap (B)': fund['Market_Cap'],
        })
        if usar_api_real:
            time.sleep(0.1)
    return pd.DataFrame(datos)

# RENDERIZADO DE TABLAS

def mostrar_tabla(df):
    html = df.to_html(escape=False, index=False)
    st.markdown(html, unsafe_allow_html=True)

# SISTEMA DE ALERTAS CON UUID

def inicializar_alertas():
    if 'alertas' not in st.session_state:
        st.session_state.alertas = []
        st.session_state.historial_alertas = []

def agregar_alerta(ticker, precio_obj, tipo, comentario=""):
    nueva = {
        'id': uuid.uuid4().hex,
        'ticker': ticker,
        'precio_obj': precio_obj,
        'tipo': tipo,
        'comentario': comentario,
        'activa': True,
        'creada': datetime.now()
    }
    st.session_state.alertas.append(nueva)

def eliminar_alerta(alerta_id):
    st.session_state.alertas = [a for a in st.session_state.alertas if a['id'] != alerta_id]

def verificar_alertas(df):
    activadas = []
    for alerta in st.session_state.alertas:
        if not alerta['activa']: continue
        fila = df[df['Ticker']==alerta['ticker']]
        if not fila.empty:
            precio_act = float(re.sub(r'[^\d\.]','', fila.iloc[0]['Precio Actual']))
            cond = (alerta['tipo']=='subida' and precio_act>=alerta['precio_obj']) or (
                   alerta['tipo']=='bajada' and precio_act<=alerta['precio_obj'])
            if cond:
                alerta['activa'] = False
                alerta['activada'] = datetime.now()
                alerta['precio_final'] = precio_act
                st.session_state.historial_alertas.append(alerta.copy())
                activadas.append(alerta)
    return activadas

# SIDEBAR
with st.sidebar:
    st.markdown("### 🎯 Configuración del Análisis")
    indice = st.selectbox("📈 Selecciona el mercado:", ["S&P 500","IBEX 35","Mercados Asiáticos","Criptomonedas"] )
    filtro = st.text_input("🔍 Buscar acciones:")
    usar_api = st.checkbox("📡 Usar datos reales (API)", value=False)
    mostrar_grafs = st.checkbox("📊 Mostrar gráficos", value=True)
    num_acc = st.slider("📋 Número de acciones a mostrar:",10,50,20)
    if st.button("🔄 Actualizar Precios"):
        cache_precios.clear()
        st.rerun()
    st.markdown("### 🚨 Sistema de Alertas")
    inicializar_alertas()
    with st.expander("➕ Crear Nueva Alerta"):
        tck = st.text_input("Ticker:").upper()
        tp = st.selectbox("Tipo:",["subida","bajada"])
        po = st.number_input("Precio objetivo:",min_value=0.000001,step=0.01,format="%.6f")
        com = st.text_area("Comentario (opcional):")
        if st.button("🔔 Crear Alerta"):
            if tck and po>0:
                agregar_alerta(tck,po,tp,com)
                st.success(f"✅ Alerta creada para {tck}")
                st.rerun()
            else:
                st.error("❌ Completa los campos obligatorios")

# CONTENIDO PRINCIPAL
render_header()
render_styles()
st.markdown("### 📊 Panel de Análisis Avanzado de Acciones")
tickers = obtener_tickers(indice)
df = obtener_datos_acciones(tickers[:num_acc], filtro, usar_api)

alertas_activadas = verificar_alertas(df)
for a in alertas_activadas:
    tipo_em = '⬆️' if a['tipo']=='subida' else '⬇️'
    st.markdown(f"**{tipo_em} Alerta activada para {a['ticker']}! Precio: {a['precio_final']}**")

if df.empty:
    st.warning("No se encontraron acciones con los filtros seleccionados.")
else:
    mostrar_tabla(df)

    # Métricas agregadas
    gan_med = df['Ganancia Potencial'].str.rstrip('%').astype(float).mean()
    num_compra = (df['Recomendación']=='📈 COMPRA').sum() + (df['Recomendación']=='🚀 COMPRA FUERTE').sum()
    num_venta = (df['Recomendación']=='📉 VENDER').sum()
    st.metric("Ganancia Potencial Media", f"{gan_med:.1f}%")
    st.metric("Oportunidades de Compra", num_compra)
    st.metric("Recomendaciones de Venta", num_venta)

    if mostrar_grafs:
        fig, ax = plt.subplots()
        ax.bar(df['Ticker'], df['Ganancia Potencial'].str.rstrip('%').astype(float))
        ax.set_xticklabels(df['Ticker'], rotation=45)
        st.pyplot(fig)

# FOOTER
st.markdown(
    """
    <div style='text-align: center; margin-top: 2rem;'>
        <b>Oráculo de Omaha</b> no está afiliado a Warren Buffett ni a Berkshire Hathaway.<br>
        Esta app es solo para fines educativos y de entretenimiento.<br>
        <b>No constituye asesoramiento financiero.</b>
    </div>
    """, unsafe_allow_html=True
)
