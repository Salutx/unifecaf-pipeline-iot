
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Dashboard IoT", page_icon="🌡️", layout="wide")

DB_USER     = os.getenv("DB_USER", "iot_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iot_senha123")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "iot_db")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

@st.cache_data(ttl=60)
def load_view(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", get_engine())

st.title("🌡️ Dashboard de Temperaturas IoT")
st.markdown("Análise dos dados coletados por sensores IoT de temperatura — UniFECAF")

try:
    with get_engine().connect():
        pass
    st.success("✅ Conectado ao PostgreSQL!")
except Exception as e:
    st.error(f"❌ Erro de conexão: {e}")
    st.info("Execute: `docker compose up -d` e depois `python src/ingest.py`")
    st.stop()

st.divider()

st.subheader("📊 Resumo Geral")
try:
    df_disp = load_view("avg_temp_por_dispositivo")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Dispositivos IoT", f"{len(df_disp):,}")
    c2.metric("Total de Leituras", f"{df_disp['total_leituras'].sum():,}")
    c3.metric("Temperatura Média", f"{df_disp['avg_temp'].mean():.1f} °C")
    c4.metric("Amplitude Máxima", f"{df_disp['max_temp'].max() - df_disp['min_temp'].min():.1f} °C")
except Exception as e:
    st.warning(f"Métricas indisponíveis: {e}")

st.divider()

st.subheader("📍 Gráfico 1 — Temperatura Média por Dispositivo")
st.caption("View: avg_temp_por_dispositivo")
try:
    df_avg = load_view("avg_temp_por_dispositivo")
    fig1 = px.bar(df_avg, x="device_id", y="avg_temp",
                  color="avg_temp", color_continuous_scale="RdYlGn_r",
                  labels={"device_id": "Dispositivo", "avg_temp": "Temperatura Média (°C)"},
                  title="Temperatura Média por Dispositivo IoT")
    fig1.update_layout(xaxis_tickangle=-45, height=450)
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("Ver dados"):
        st.dataframe(df_avg, use_container_width=True)
except Exception as e:
    st.error(f"Erro: {e}")

st.divider()

st.subheader("🕐 Gráfico 2 — Leituras e Temperatura por Hora do Dia")
st.caption("View: leituras_por_hora")
try:
    df_hora = load_view("leituras_por_hora")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_hora["hora"], y=df_hora["contagem"],
                          name="Nº de Leituras", marker_color="steelblue", yaxis="y1"))
    fig2.add_trace(go.Scatter(x=df_hora["hora"], y=df_hora["avg_temp_hora"],
                              name="Temp. Média (°C)", mode="lines+markers",
                              line=dict(color="tomato", width=2), yaxis="y2"))
    fig2.update_layout(
        title="Atividade dos Sensores por Hora",
        xaxis=dict(title="Hora", dtick=1),
        yaxis=dict(title="Contagem"),
        yaxis2=dict(title="Temperatura (°C)", overlaying="y", side="right"),
        height=450)
    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("Ver dados"):
        st.dataframe(df_hora, use_container_width=True)
except Exception as e:
    st.error(f"Erro: {e}")

st.divider()

st.subheader("📅 Gráfico 3 — Variação Diária de Temperatura")
st.caption("View: temp_max_min_por_dia")
try:
    df_dia = load_view("temp_max_min_por_dia")
    df_dia["data"] = pd.to_datetime(df_dia["data"])
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_dia["data"], y=df_dia["temp_max"], name="Máxima",
                              mode="lines", line=dict(color="red", width=1.5)))
    fig3.add_trace(go.Scatter(x=df_dia["data"], y=df_dia["temp_media"], name="Média",
                              mode="lines", line=dict(color="orange", width=2),
                              fill="tonexty", fillcolor="rgba(255,100,100,0.15)"))
    fig3.add_trace(go.Scatter(x=df_dia["data"], y=df_dia["temp_min"], name="Mínima",
                              mode="lines", line=dict(color="royalblue", width=1.5),
                              fill="tonexty", fillcolor="rgba(100,149,237,0.15)"))
    fig3.update_layout(title="Temperaturas Máx/Média/Mín por Dia",
                       xaxis_title="Data", yaxis_title="Temperatura (°C)",
                       hovermode="x unified", height=450)
    st.plotly_chart(fig3, use_container_width=True)
    with st.expander("Ver dados"):
        st.dataframe(df_dia, use_container_width=True)
except Exception as e:
    st.error(f"Erro: {e}")

st.divider()

st.subheader("💡 Principais Insights")
st.markdown("""
| # | Insight | Aplicação Prática |
|---|---------|-------------------|
| 1 | Dispositivos com temperatura média elevada podem indicar falhas ou ambientes críticos | Manutenção preditiva |
| 2 | Picos de leitura em horários específicos revelam padrões operacionais dos ambientes | Otimização de climatização |
| 3 | Grandes amplitudes térmicas diárias podem sinalizar falhas em sensores | Alertas automáticos |
| 4 | Tendências temporais permitem planejar manutenção preventiva | Planejamento de capacidade |
""")
st.caption("Pipeline IoT — Disruptive Architectures: IoT, Big Data e IA — UniFECAF")
