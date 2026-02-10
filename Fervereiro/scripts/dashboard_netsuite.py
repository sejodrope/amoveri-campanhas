"""
Dashboard de Gestão Comercial - NetSuite DRE
Amoveri Farma

Baseado nos dados do NetSuite (DRE Gerencial)
Versão 5.0 - Completo com Análise ABC, Mapa, Evolução Mensal,
             Performance de Vendedores, Contratos e Export

Autor: José Pedro Vieira Silva
Data: 10/02/2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from datetime import datetime
from io import BytesIO
import base64

# Configuração da página
st.set_page_config(
    page_title="Dashboard Comercial - Amoveri Farma",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background: #f0f2f6; }
    .block-container {
        padding: 1.5rem 2rem;
        max-width: 1400px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem 0.8rem;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex; justify-content: center; padding: 0.5rem 0;
    }
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700; font-size: 2rem; margin-bottom: 0.2rem;
    }
    h2 { color: #2d3748; font-weight: 600; font-size: 1.5rem; margin-top: 1.2rem; margin-bottom: 0.6rem; }
    h3 { color: #4a5568; font-weight: 600; font-size: 1.1rem; margin-top: 0.8rem; }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem; font-weight: 600; color: #4a5568;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    div[data-testid="column"] > div {
        background: white; padding: 0.8rem; border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }
    .js-plotly-plot { border-radius: 10px; overflow: hidden; }
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
    hr { margin: 1.2rem 0; border: none; height: 1px; background: #e2e8f0; }
    .stAlert { border-radius: 8px; border-left: 4px solid #667eea; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0; padding: 8px 16px;
        font-weight: 600; font-size: 0.9rem;
    }
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px;
        font-weight: 600; font-size: 0.85rem;
    }
    [data-testid="stDownloadButton"] button:hover { opacity: 0.9; }
    @media (max-width: 768px) {
        .block-container { padding: 0.5rem; }
        h1 { font-size: 1.4rem; } h2 { font-size: 1.2rem; }
        [data-testid="stMetricValue"] { font-size: 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# Coordenadas dos estados brasileiros (capitais) para o mapa
COORDS_UF = {
    'AC': (-9.97, -67.81), 'AL': (-9.57, -36.78), 'AM': (-3.12, -60.02),
    'AP': (0.03, -51.05), 'BA': (-12.97, -38.51), 'CE': (-3.72, -38.54),
    'DF': (-15.78, -47.93), 'ES': (-20.32, -40.34), 'GO': (-16.68, -49.25),
    'MA': (-2.53, -44.28), 'MG': (-19.92, -43.94), 'MS': (-20.44, -54.65),
    'MT': (-15.60, -56.10), 'PA': (-1.46, -48.50), 'PB': (-7.12, -34.86),
    'PE': (-8.05, -34.87), 'PI': (-5.09, -42.80), 'PR': (-25.43, -49.27),
    'RJ': (-22.91, -43.17), 'RN': (-5.79, -35.21), 'RO': (-8.76, -63.90),
    'RR': (2.82, -60.67), 'RS': (-30.03, -51.23), 'SC': (-27.60, -48.55),
    'SE': (-10.91, -37.07), 'SP': (-23.55, -46.63), 'TO': (-10.18, -48.33)
}

# Diretórios
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database" / "campanhas"
LOGO_PATH = BASE_DIR / "LOGO AMOVERI FARMA.png"


def limpar_valor(valor_str):
    """Converte string de valor em float"""
    if not valor_str or pd.isna(valor_str):
        return 0.0
    valor = str(valor_str).replace('R$', '').replace('"', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(valor)
    except:
        return 0.0


def calcular_trimestre(data_str):
    """Calcula o trimestre a partir da data"""
    try:
        mes = pd.to_datetime(data_str, format='%d/%m/%Y').month
        if mes <= 3: return 'Q1'
        elif mes <= 6: return 'Q2'
        elif mes <= 9: return 'Q3'
        else: return 'Q4'
    except:
        return 'N/A'


def classificar_abc(df_sorted, col_valor):
    """Classifica itens em A, B, C (Pareto 80/15/5)"""
    total = df_sorted[col_valor].sum()
    if total == 0:
        df_sorted['Classe_ABC'] = 'C'
        return df_sorted
    df_sorted['Pct_Acumulado'] = df_sorted[col_valor].cumsum() / total * 100
    df_sorted['Classe_ABC'] = df_sorted['Pct_Acumulado'].apply(
        lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C')
    )
    return df_sorted


def gerar_csv_download(df, nome_arquivo):
    """Gera botão de download CSV"""
    csv = df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    st.download_button(
        label="Baixar dados (CSV)",
        data=csv,
        file_name=nome_arquivo,
        mime='text/csv'
    )


# Layout padrão para gráficos Plotly
PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color="#2d3748"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="#f0f0f0", zerolinecolor="#e0e0e0", tickfont=dict(color="#2d3748")),
    yaxis=dict(gridcolor="#f0f0f0", zerolinecolor="#e0e0e0", tickfont=dict(color="#2d3748")),
)


@st.cache_data
def carregar_dre_netsuite():
    """Carrega dados do DRE NetSuite"""
    file_path = DATABASE_DIR / "CTR- BASE VENDAS DRE GERENCIAL - 10.25-10.02.26.csv"

    df = pd.read_csv(file_path, encoding='latin-1', skiprows=6)
    df.columns = df.columns.str.strip()

    # Valores float
    df['Fat_Bruto_Float'] = df['Faturamento Bruto'].apply(limpar_valor)
    df['Fat_Liquido_Float'] = df['Faturamento Liquido'].apply(limpar_valor)

    # Quantidade
    df['Quantidade'] = df['Quantidade'].astype(str).str.replace(',', '').str.strip()
    df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(0).astype(int)

    # Datas
    df['Data_DT'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    df['Mes_Ano'] = df['Data_DT'].dt.to_period('M').astype(str)
    df['Mes_Num'] = df['Data_DT'].dt.month
    df['Ano'] = df['Data_DT'].dt.year
    df['Trimestre'] = df['Data'].apply(calcular_trimestre)

    # Mês por extenso
    meses_pt = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    df['Mes_Nome'] = df['Mes_Num'].map(meses_pt).fillna('N/A') + '/' + df['Ano'].astype(str).str[-2:]

    # Encontrar coluna REGIÃO (pode ter encoding diferente)
    regiao_col = [c for c in df.columns if 'REGI' in c.upper()]
    if regiao_col:
        df = df.rename(columns={regiao_col[0]: 'REGIÃO'})

    # Campos vazios
    df['UF1'] = df['UF1'].fillna('SEM UF')
    df['REGIÃO'] = df['REGIÃO'].fillna('SEM REGIÃO')
    df['GRUPO DO CLIENTE'] = df['GRUPO DO CLIENTE'].fillna('SEM GRUPO')
    df['Parceiro: Representante de vendas'] = df['Parceiro: Representante de vendas'].fillna('SEM PARCEIRO')
    df['Canal de Venda utilizado'] = df['Canal de Venda utilizado'].fillna('SEM CANAL')
    # Normalizar PEDIDO DE CONTRATO (encoding pode vir quebrado)
    df['PEDIDO DE CONTRATO'] = df['PEDIDO DE CONTRATO'].apply(
        lambda x: 'Sim' if str(x).strip() == 'Sim' else 'Não'
    )
    df['Representante de vendas'] = df['Representante de vendas'].fillna('SEM VENDEDOR')
    df['Item: Fabricante'] = df['Item: Fabricante'].fillna('SEM FABRICANTE')

    # Categorizar SEM GRUPO: usar nome da empresa
    mask_sem_grupo = df['GRUPO DO CLIENTE'] == 'SEM GRUPO'
    df.loc[mask_sem_grupo, 'GRUPO DO CLIENTE'] = df.loc[mask_sem_grupo, 'Cliente: Tarefa']

    # Renomear colunas
    df = df.rename(columns={
        'Cliente: Tarefa': 'Cliente',
        'Parceiro: Representante de vendas': 'Parceiro',
        'Canal de Venda utilizado': 'Canal',
        'Representante de vendas': 'Vendedor',
        'Item: Nome': 'Produto',
        'Item: Fabricante': 'Fabricante',
        'Categoria de cliente: Nome': 'Categoria',
        'UF1': 'UF',
        'REGIÃO': 'Regiao'
    })

    return df


# ========================
# HEADER
# ========================
st.title("Dashboard de Gestão Comercial")
st.markdown("---")

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    try:
        from PIL import Image
        logo_img = Image.open(LOGO_PATH)
        logo_img = logo_img.resize((400, int(400 * logo_img.height / logo_img.width)))
        st.image(logo_img, use_container_width=True)
    except Exception:
        st.markdown("### Amoveri Farma")
    st.caption("Dashboard Comercial")

    st.markdown("---")

    with st.spinner("Carregando dados..."):
        df = carregar_dre_netsuite()

    meses_pt_sidebar = {1:'Jan',2:'Fev',3:'Mar',4:'Abr',5:'Mai',6:'Jun',7:'Jul',8:'Ago',9:'Set',10:'Out',11:'Nov',12:'Dez'}
    data_min = df['Data_DT'].min()
    data_max = df['Data_DT'].max()
    periodo_inicio = f"{meses_pt_sidebar[data_min.month]}/{data_min.year}"
    periodo_fim = f"{meses_pt_sidebar[data_max.month]}/{data_max.year}"
    st.markdown(f"**Período:** {periodo_inicio} - {periodo_fim}")
    st.caption(f"{len(df):,} registros carregados")

    st.markdown("---")

    # Filtros
    trimestres = ['Todos'] + sorted(df['Trimestre'].unique().tolist())
    trimestre_selecionado = st.selectbox("Trimestre", trimestres, index=0)

    ufs_disponiveis = ['Todos'] + sorted(df['UF'].unique().tolist())
    uf_selecionada = st.selectbox("Estado (UF)", ufs_disponiveis, index=0)

    parceiros = ['Todos'] + sorted(df['Parceiro'].unique().tolist())
    parceiro_selecionado = st.selectbox("Parceiro", parceiros, index=0)

    canais = ['Todos'] + sorted(df['Canal'].unique().tolist())
    canal_selecionado = st.selectbox("Canal de Venda", canais, index=0)

    st.markdown("---")

    st.markdown("**Visões**")
    visao = st.radio(
        "Visões:",
        [
            "📈 Visão Geral",
            "📅 Evolução Mensal",
            "🏢 Análise por Grupo",
            "📊 Análise ABC",
            "📺 Análise por Canal",
            "🤝 Análise por Parceiro",
            "🏭 Análise por Laboratório",
            "👤 Performance Vendedores",
            "📋 Análise de Contratos"
        ],
        label_visibility="collapsed"
    )
    visao = visao.split(" ", 1)[1] if " " in visao else visao

# Aplicar filtros
df_filtrado = df.copy()
if trimestre_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Trimestre'] == trimestre_selecionado]
if uf_selecionada != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['UF'] == uf_selecionada]
if parceiro_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Parceiro'] == parceiro_selecionado]
if canal_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Canal'] == canal_selecionado]

if len(df_filtrado) < len(df):
    st.info(f"Exibindo **{len(df_filtrado):,}** de {len(df):,} registros (filtros aplicados)")


# ========================
# VISÃO GERAL
# ========================
if visao == "Visão Geral":
    st.markdown("## 📈 Visão Geral do Negócio")

    total_fat_bruto = df_filtrado['Fat_Bruto_Float'].sum()
    total_fat_liquido = df_filtrado['Fat_Liquido_Float'].sum()
    num_transacoes = len(df_filtrado)
    ticket_medio = total_fat_liquido / num_transacoes if num_transacoes > 0 else 0
    num_clientes = df_filtrado['Cliente'].nunique()
    num_produtos = df_filtrado['Produto'].nunique()
    qtd_total = df_filtrado['Quantidade'].sum()
    num_fabricantes = df_filtrado['Fabricante'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Fat. Bruto", f"R$ {total_fat_bruto/1e6:.2f}M")
    with col2:
        st.metric("💵 Fat. Líquido", f"R$ {total_fat_liquido/1e6:.2f}M")
    with col3:
        st.metric("🎯 Ticket Médio", f"R$ {ticket_medio/1e3:.1f}k")
    with col4:
        st.metric("📊 Transações", f"{num_transacoes:,}")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("👥 Clientes", f"{num_clientes:,}")
    with col6:
        st.metric("📦 Produtos", f"{num_produtos:,}")
    with col7:
        st.metric("🔢 Qtd. Vendida", f"{qtd_total:,}")
    with col8:
        st.metric("🏭 Laboratórios", f"{num_fabricantes}")

    # Contratos resumo
    transacoes_contrato = df_filtrado[df_filtrado['PEDIDO DE CONTRATO'] == 'Sim']
    num_contratos = len(transacoes_contrato)
    pct_contratos = (num_contratos / num_transacoes * 100) if num_transacoes > 0 else 0
    fat_contratos = transacoes_contrato['Fat_Liquido_Float'].sum()
    pct_fat_contratos = (fat_contratos / total_fat_liquido * 100) if total_fat_liquido > 0 else 0

    col9, col10, col11 = st.columns(3)
    with col9:
        st.metric("📋 Transações c/ Contrato", f"{num_contratos:,}", f"{pct_contratos:.1f}% do total")
    with col10:
        st.metric("💼 Fat. via Contratos", f"R$ {fat_contratos/1e6:.2f}M", f"{pct_fat_contratos:.1f}% do total")
    with col11:
        clientes_contrato = transacoes_contrato['Cliente'].nunique() if num_contratos > 0 else 0
        st.metric("👥 Clientes c/ Contrato", f"{clientes_contrato}")

    st.markdown("---")

    # Mini evolução mensal + Mapa
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Evolução Mensal")
        fat_mensal = df_filtrado.groupby('Mes_Ano')['Fat_Liquido_Float'].sum().reset_index()
        fat_mensal = fat_mensal.sort_values('Mes_Ano')
        fat_mensal['Mes_Label'] = fat_mensal['Mes_Ano'].apply(
            lambda x: f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][int(x.split('-')[1])-1]}/{x.split('-')[0][-2:]}"
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fat_mensal['Mes_Label'], y=fat_mensal['Fat_Liquido_Float'],
            mode='lines+markers+text',
            text=[f"R$ {v/1e6:.1f}M" for v in fat_mensal['Fat_Liquido_Float']],
            textposition='top center', textfont=dict(size=10),
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#667eea')
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=400, showlegend=False,
                          yaxis_title="Faturamento (R$)", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Mapa de Vendas por UF")
        fat_uf = df_filtrado.groupby('UF')['Fat_Liquido_Float'].sum().reset_index()
        fat_uf = fat_uf[fat_uf['UF'] != 'SEM UF']
        fat_uf['lat'] = fat_uf['UF'].map(lambda x: COORDS_UF.get(x, (0, 0))[0])
        fat_uf['lon'] = fat_uf['UF'].map(lambda x: COORDS_UF.get(x, (0, 0))[1])
        fat_uf = fat_uf[fat_uf['lat'] != 0]

        max_fat = fat_uf['Fat_Liquido_Float'].max()
        fat_uf['size'] = (fat_uf['Fat_Liquido_Float'] / max_fat * 50).clip(lower=5) if max_fat > 0 else 10
        fat_uf['texto'] = fat_uf.apply(lambda r: f"{r['UF']}: R$ {r['Fat_Liquido_Float']/1e6:.1f}M", axis=1)

        fig = go.Figure()
        fig.add_trace(go.Scattergeo(
            lat=fat_uf['lat'], lon=fat_uf['lon'],
            text=fat_uf['texto'], hoverinfo='text',
            marker=dict(
                size=fat_uf['size'],
                color=fat_uf['Fat_Liquido_Float'],
                colorscale='Purples', showscale=True,
                colorbar=dict(title="Fat. (R$)"),
                line=dict(width=1, color='white')
            )
        ))
        fig.update_geos(
            scope='south america',
            showland=True, landcolor='rgb(243, 243, 243)',
            showocean=True, oceancolor='rgb(204, 224, 245)',
            showcountries=True, countrycolor='rgb(204, 204, 204)',
            showcoastlines=True, coastlinecolor='rgb(204, 204, 204)',
            fitbounds='locations'
        )
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)


# ========================
# EVOLUÇÃO MENSAL
# ========================
elif visao == "Evolução Mensal":
    st.markdown("## 📅 Evolução Mensal")

    mensal = df_filtrado.groupby('Mes_Ano').agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Cliente': 'nunique',
        'Produto': 'nunique',
        'Quantidade': 'sum'
    }).reset_index()
    mensal = mensal.sort_values('Mes_Ano')
    mensal.columns = ['Mes_Ano', 'Fat_Bruto', 'Fat_Liquido', 'Clientes', 'Produtos', 'Quantidade']

    # Label amigável
    mensal['Mes_Label'] = mensal['Mes_Ano'].apply(
        lambda x: f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][int(x.split('-')[1])-1]}/{x.split('-')[0][-2:]}"
    )

    # Variação mês a mês
    mensal['Variacao'] = mensal['Fat_Liquido'].pct_change() * 100

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Faturamento Mensal")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mensal['Mes_Label'], y=mensal['Fat_Bruto'],
            name='Bruto', marker_color='#a3bffa'
        ))
        fig.add_trace(go.Bar(
            x=mensal['Mes_Label'], y=mensal['Fat_Liquido'],
            name='Líquido', marker_color='#667eea'
        ))
        fig.update_layout(**PLOTLY_LAYOUT, barmode='group', height=400,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Variação Mês a Mês (%)")
        var_data = mensal.dropna(subset=['Variacao'])
        cores = ['#48bb78' if v >= 0 else '#f56565' for v in var_data['Variacao']]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=var_data['Mes_Label'], y=var_data['Variacao'],
            marker_color=cores,
            text=[f"{v:+.1f}%" for v in var_data['Variacao']],
            textposition='outside'
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=400, yaxis_title="Variação (%)")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Clientes Ativos por Mês")
        fig = px.area(
            mensal, x='Mes_Label', y='Clientes',
            labels={'Clientes': 'Clientes Ativos', 'Mes_Label': ''},
            color_discrete_sequence=['#48bb78']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("### Quantidade Vendida por Mês")
        fig = px.area(
            mensal, x='Mes_Label', y='Quantidade',
            labels={'Quantidade': 'Unidades', 'Mes_Label': ''},
            color_discrete_sequence=['#ed8936']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Detalhamento Mensal")
    tabela_mensal = mensal.copy()
    tabela_mensal['Fat_Bruto'] = tabela_mensal['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela_mensal['Fat_Liquido'] = tabela_mensal['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    tabela_mensal['Variacao'] = tabela_mensal['Variacao'].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
    tabela_mensal['Quantidade'] = tabela_mensal['Quantidade'].apply(lambda x: f"{x:,}")

    st.dataframe(
        tabela_mensal[['Mes_Label', 'Fat_Bruto', 'Fat_Liquido', 'Variacao', 'Clientes', 'Produtos', 'Quantidade']].rename(
            columns={'Mes_Label': 'Mês', 'Variacao': 'Var. %'}
        ),
        use_container_width=True
    )
    gerar_csv_download(mensal[['Mes_Ano', 'Fat_Bruto', 'Fat_Liquido', 'Clientes', 'Produtos', 'Quantidade']],
                       "evolucao_mensal.csv")


# ========================
# ANÁLISE POR GRUPO
# ========================
elif visao == "Análise por Grupo":
    st.markdown("## 🏢 Análise por Grupo de Cliente")

    grupo_stats = df_filtrado.groupby('GRUPO DO CLIENTE').agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Cliente': 'nunique'
    }).reset_index()
    grupo_stats.columns = ['Grupo', 'Fat_Bruto', 'Fat_Liquido', 'Num_Clientes']
    grupo_stats = grupo_stats.sort_values('Fat_Liquido', ascending=False)

    total = grupo_stats['Fat_Liquido'].sum()
    top3 = (grupo_stats.head(3)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0
    top5 = (grupo_stats.head(5)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0
    top10 = (grupo_stats.head(10)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Grupos", f"{len(grupo_stats)}")
    with col2:
        st.metric("🥇 Top 3", f"{top3:.1f}%")
    with col3:
        st.metric("🥈 Top 5", f"{top5:.1f}%")
    with col4:
        st.metric("🥉 Top 10", f"{top10:.1f}%")

    if top3 > 40:
        st.warning("Alta concentração nos top 3 grupos - risco de dependência")

    st.markdown("---")

    st.markdown("### Top 15 Grupos por Faturamento")
    fig = px.bar(
        grupo_stats.head(15), y='Grupo', x='Fat_Liquido', orientation='h',
        labels={'Fat_Liquido': 'Faturamento Líquido (R$)', 'Grupo': ''},
        color='Fat_Liquido', color_continuous_scale='Purples'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=550, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Tabela Completa")
    top_grupos = grupo_stats.head(30).copy()
    top_grupos_export = top_grupos.copy()
    top_grupos['Fat_Bruto'] = top_grupos['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    top_grupos['Fat_Liquido'] = top_grupos['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")

    st.dataframe(
        top_grupos[['Grupo', 'Num_Clientes', 'Fat_Liquido', 'Fat_Bruto']].rename(columns={'Num_Clientes': 'Clientes'}),
        use_container_width=True, height=600
    )
    gerar_csv_download(top_grupos_export, "grupos_clientes.csv")


# ========================
# ANÁLISE ABC
# ========================
elif visao == "Análise ABC":
    st.markdown("## 📊 Análise ABC (Pareto)")
    st.caption("Classificação: **A** = 80% do faturamento | **B** = próximos 15% | **C** = últimos 5%")

    tab_abc1, tab_abc2, tab_abc3 = st.tabs(["🏢 ABC Clientes", "📦 ABC Produtos", "🏭 ABC Laboratórios"])

    # --- ABC CLIENTES ---
    with tab_abc1:
        cliente_fat = df_filtrado.groupby('Cliente').agg({
            'Fat_Liquido_Float': 'sum',
            'Quantidade': 'sum',
            'Produto': 'nunique'
        }).reset_index()
        cliente_fat.columns = ['Cliente', 'Fat_Liquido', 'Quantidade', 'Num_Produtos']
        cliente_fat = cliente_fat.sort_values('Fat_Liquido', ascending=False).reset_index(drop=True)
        cliente_fat = classificar_abc(cliente_fat, 'Fat_Liquido')

        contagem = cliente_fat['Classe_ABC'].value_counts()
        fat_classe = cliente_fat.groupby('Classe_ABC')['Fat_Liquido'].sum()

        col1, col2, col3 = st.columns(3)
        for i, (classe, col) in enumerate(zip(['A', 'B', 'C'], [col1, col2, col3])):
            n = contagem.get(classe, 0)
            f = fat_classe.get(classe, 0)
            pct = (n / len(cliente_fat) * 100) if len(cliente_fat) > 0 else 0
            with col:
                st.metric(f"Classe {classe}", f"{n} clientes ({pct:.0f}%)",
                          f"R$ {f/1e6:.2f}M")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Curva ABC - Clientes")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(cliente_fat)+1)),
                y=cliente_fat['Pct_Acumulado'],
                mode='lines', line=dict(color='#667eea', width=2),
                fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.1)'
            ))
            fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% (A)")
            fig.add_hline(y=95, line_dash="dash", line_color="orange", annotation_text="95% (B)")
            fig.update_layout(height=400, xaxis_title="Clientes (ordenados por faturamento)",
                              yaxis_title="% Acumulado do Faturamento")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Distribuição por Classe")
            dist = pd.DataFrame({
                'Classe': ['A', 'B', 'C'],
                'Clientes': [contagem.get('A', 0), contagem.get('B', 0), contagem.get('C', 0)],
                'Faturamento': [fat_classe.get('A', 0), fat_classe.get('B', 0), fat_classe.get('C', 0)]
            })
            fig = px.bar(dist, x='Classe', y='Faturamento',
                         color='Classe', color_discrete_map={'A': '#48bb78', 'B': '#ed8936', 'C': '#f56565'},
                         text=[f"R$ {v/1e6:.1f}M" for v in dist['Faturamento']])
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Clientes Classe A (Top)")
        classe_a = cliente_fat[cliente_fat['Classe_ABC'] == 'A'].copy()
        classe_a_export = classe_a.copy()
        classe_a['Fat_Liquido'] = classe_a['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        classe_a['Pct_Acumulado'] = classe_a['Pct_Acumulado'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(
            classe_a[['Cliente', 'Num_Produtos', 'Quantidade', 'Fat_Liquido', 'Pct_Acumulado', 'Classe_ABC']].rename(
                columns={'Num_Produtos': 'Produtos', 'Pct_Acumulado': '% Acum.', 'Classe_ABC': 'Classe'}
            ),
            use_container_width=True, height=500
        )
        gerar_csv_download(classe_a_export, "abc_clientes.csv")

    # --- ABC PRODUTOS ---
    with tab_abc2:
        produto_fat = df_filtrado.groupby(['Produto', 'Fabricante']).agg({
            'Fat_Liquido_Float': 'sum',
            'Quantidade': 'sum',
            'Cliente': 'nunique'
        }).reset_index()
        produto_fat.columns = ['Produto', 'Fabricante', 'Fat_Liquido', 'Quantidade', 'Num_Clientes']
        produto_fat = produto_fat.sort_values('Fat_Liquido', ascending=False).reset_index(drop=True)
        produto_fat = classificar_abc(produto_fat, 'Fat_Liquido')

        contagem_p = produto_fat['Classe_ABC'].value_counts()
        fat_classe_p = produto_fat.groupby('Classe_ABC')['Fat_Liquido'].sum()

        col1, col2, col3 = st.columns(3)
        for classe, col in zip(['A', 'B', 'C'], [col1, col2, col3]):
            n = contagem_p.get(classe, 0)
            f = fat_classe_p.get(classe, 0)
            pct = (n / len(produto_fat) * 100) if len(produto_fat) > 0 else 0
            with col:
                st.metric(f"Classe {classe}", f"{n} produtos ({pct:.0f}%)", f"R$ {f/1e6:.2f}M")

        st.markdown("### Curva ABC - Produtos")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(produto_fat)+1)),
            y=produto_fat['Pct_Acumulado'],
            mode='lines', line=dict(color='#764ba2', width=2),
            fill='tozeroy', fillcolor='rgba(118, 75, 162, 0.1)'
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% (A)")
        fig.add_hline(y=95, line_dash="dash", line_color="orange", annotation_text="95% (B)")
        fig.update_layout(height=350, xaxis_title="Produtos (ordenados por faturamento)",
                          yaxis_title="% Acumulado")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Produtos Classe A")
        classe_a_p = produto_fat[produto_fat['Classe_ABC'] == 'A'].copy()
        classe_a_p_export = classe_a_p.copy()
        classe_a_p['Fat_Liquido'] = classe_a_p['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        classe_a_p['Pct_Acumulado'] = classe_a_p['Pct_Acumulado'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(
            classe_a_p[['Produto', 'Fabricante', 'Num_Clientes', 'Quantidade', 'Fat_Liquido', 'Pct_Acumulado']].rename(
                columns={'Num_Clientes': 'Clientes', 'Pct_Acumulado': '% Acum.'}
            ),
            use_container_width=True, height=500
        )
        gerar_csv_download(classe_a_p_export, "abc_produtos.csv")

    # --- ABC LABORATÓRIOS ---
    with tab_abc3:
        lab_fat = df_filtrado.groupby('Fabricante').agg({
            'Fat_Liquido_Float': 'sum',
            'Produto': 'nunique',
            'Cliente': 'nunique',
            'Quantidade': 'sum'
        }).reset_index()
        lab_fat.columns = ['Laboratório', 'Fat_Liquido', 'Num_Produtos', 'Num_Clientes', 'Quantidade']
        lab_fat = lab_fat.sort_values('Fat_Liquido', ascending=False).reset_index(drop=True)
        lab_fat = classificar_abc(lab_fat, 'Fat_Liquido')

        contagem_l = lab_fat['Classe_ABC'].value_counts()

        col1, col2, col3 = st.columns(3)
        for classe, col in zip(['A', 'B', 'C'], [col1, col2, col3]):
            n = contagem_l.get(classe, 0)
            with col:
                labs = lab_fat[lab_fat['Classe_ABC'] == classe]['Laboratório'].tolist()
                st.metric(f"Classe {classe}", f"{n} laboratórios")
                if labs:
                    st.caption(", ".join(labs[:5]) + ("..." if len(labs) > 5 else ""))

        st.markdown("### Tabela ABC - Laboratórios")
        lab_fat_display = lab_fat.copy()
        lab_fat_export = lab_fat.copy()
        lab_fat_display['Fat_Liquido'] = lab_fat_display['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        lab_fat_display['Pct_Acumulado'] = lab_fat_display['Pct_Acumulado'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(
            lab_fat_display[['Laboratório', 'Classe_ABC', 'Num_Produtos', 'Num_Clientes', 'Quantidade', 'Fat_Liquido', 'Pct_Acumulado']].rename(
                columns={'Classe_ABC': 'Classe', 'Num_Produtos': 'Produtos', 'Num_Clientes': 'Clientes', 'Pct_Acumulado': '% Acum.'}
            ),
            use_container_width=True, height=600
        )
        gerar_csv_download(lab_fat_export, "abc_laboratorios.csv")


# ========================
# ANÁLISE POR CANAL
# ========================
elif visao == "Análise por Canal":
    st.markdown("## 📺 Análise por Canal de Venda")

    canal_stats = df_filtrado.groupby('Canal').agg({
        'Fat_Liquido_Float': 'sum', 'Cliente': 'nunique'
    }).reset_index()
    canal_stats.columns = ['Canal', 'Fat_Liquido', 'Num_Clientes']
    canal_stats['Ticket_Medio'] = canal_stats['Fat_Liquido'] / canal_stats['Num_Clientes']
    canal_stats = canal_stats.sort_values('Fat_Liquido', ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Distribuição por Canal")
        fig = px.pie(canal_stats.head(10), values='Fat_Liquido', names='Canal')
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Ticket Médio por Canal")
        fig = px.bar(
            canal_stats.head(10), x='Ticket_Medio', y='Canal', orientation='h',
            labels={'Ticket_Medio': 'Ticket Médio (R$)', 'Canal': ''},
            color='Ticket_Medio', color_continuous_scale='Oranges'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=450, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Detalhamento por Canal")
    tabela = canal_stats.copy()
    tabela_export = tabela.copy()
    tabela['Fat_Liquido'] = tabela['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Ticket_Medio'] = tabela['Ticket_Medio'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(
        tabela[['Canal', 'Num_Clientes', 'Fat_Liquido', 'Ticket_Medio']].rename(columns={'Num_Clientes': 'Clientes'}),
        use_container_width=True, height=500
    )
    gerar_csv_download(tabela_export, "analise_canal.csv")


# ========================
# ANÁLISE POR PARCEIRO
# ========================
elif visao == "Análise por Parceiro":
    st.markdown("## 🤝 Análise por Parceiro")

    parceiro_stats = df_filtrado.groupby('Parceiro').agg({
        'Fat_Liquido_Float': 'sum', 'Cliente': 'nunique'
    }).reset_index()
    parceiro_stats.columns = ['Parceiro', 'Fat_Liquido', 'Num_Clientes']
    parceiro_stats = parceiro_stats.sort_values('Fat_Liquido', ascending=False)

    num_parceiros = len(parceiro_stats[parceiro_stats['Parceiro'] != 'SEM PARCEIRO'])
    total = parceiro_stats['Fat_Liquido'].sum()
    top3 = (parceiro_stats.head(3)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Parceiros Ativos", f"{num_parceiros}")
    with col2:
        st.metric("🎯 Concentração Top 3", f"{top3:.1f}%")
    with col3:
        st.metric("💰 Fat. Total", f"R$ {total/1e6:.2f}M")

    st.markdown("---")

    st.markdown("### Top 20 Parceiros")
    fig = px.bar(
        parceiro_stats.head(20), y='Parceiro', x='Fat_Liquido', orientation='h',
        labels={'Fat_Liquido': 'Faturamento (R$)', 'Parceiro': ''},
        color='Fat_Liquido', color_continuous_scale='Viridis'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=650, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Detalhamento")
    tabela = parceiro_stats.copy()
    tabela_export = tabela.copy()
    tabela['Fat_Liquido'] = tabela['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    st.dataframe(
        tabela[['Parceiro', 'Num_Clientes', 'Fat_Liquido']].rename(columns={'Num_Clientes': 'Clientes'}),
        use_container_width=True, height=600
    )
    gerar_csv_download(tabela_export, "analise_parceiro.csv")


# ========================
# ANÁLISE POR LABORATÓRIO
# ========================
elif visao == "Análise por Laboratório":
    st.markdown("## 🏭 Análise por Laboratório")

    lab_stats = df_filtrado.groupby('Fabricante').agg({
        'Fat_Liquido_Float': 'sum', 'Produto': 'nunique',
        'Quantidade': 'sum', 'Cliente': 'nunique'
    }).reset_index()
    lab_stats.columns = ['Laboratório', 'Fat_Liquido', 'Num_Produtos', 'Quantidade', 'Num_Clientes']
    lab_stats = lab_stats.sort_values('Fat_Liquido', ascending=False)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏭 Laboratórios", f"{len(lab_stats)}")
    with col2:
        st.metric("📦 Produtos", f"{df_filtrado['Produto'].nunique()}")
    with col3:
        total_lab = lab_stats['Fat_Liquido'].sum()
        top5_pct = (lab_stats.head(5)['Fat_Liquido'].sum() / total_lab * 100) if total_lab > 0 else 0
        st.metric("🎯 Top 5", f"{top5_pct:.1f}%")
    with col4:
        st.metric("💰 Fat. Total", f"R$ {total_lab/1e6:.2f}M")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Ranking", "📦 Produtos por Lab", "👤 Lab por Vendedor", "💊 Med/Lab/Vendedor"
    ])

    with tab1:
        st.markdown("### Ranking por Faturamento")
        fig = px.bar(
            lab_stats.head(20), y='Laboratório', x='Fat_Liquido', orientation='h',
            labels={'Fat_Liquido': 'Faturamento (R$)', 'Laboratório': ''},
            color='Fat_Liquido', color_continuous_scale='Reds'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=650, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        tabela_lab = lab_stats.copy()
        tabela_lab_export = tabela_lab.copy()
        tabela_lab['Fat_Liquido_fmt'] = tabela_lab['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(
            tabela_lab[['Laboratório', 'Num_Produtos', 'Num_Clientes', 'Quantidade', 'Fat_Liquido_fmt']].rename(columns={
                'Fat_Liquido_fmt': 'Faturamento', 'Num_Produtos': 'Produtos',
                'Num_Clientes': 'Clientes', 'Quantidade': 'Qtd. Vendida'
            }),
            use_container_width=True, height=600
        )
        gerar_csv_download(tabela_lab_export, "ranking_laboratorios.csv")

    with tab2:
        lab_sel = st.selectbox("Selecione o Laboratório:", lab_stats['Laboratório'].tolist(), key='lab_prod')
        df_lab = df_filtrado[df_filtrado['Fabricante'] == lab_sel]

        prod_stats = df_lab.groupby('Produto').agg({
            'Fat_Liquido_Float': 'sum', 'Quantidade': 'sum', 'Cliente': 'nunique'
        }).reset_index()
        prod_stats.columns = ['Produto', 'Fat_Liquido', 'Quantidade', 'Num_Clientes']
        prod_stats = prod_stats.sort_values('Fat_Liquido', ascending=False)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 Produtos", f"{len(prod_stats)}")
        with col2:
            st.metric("💰 Fat. Líquido", f"R$ {prod_stats['Fat_Liquido'].sum()/1e6:.2f}M")
        with col3:
            st.metric("🔢 Qtd. Total", f"{prod_stats['Quantidade'].sum():,}")

        fig = px.bar(
            prod_stats.head(20), y='Produto', x='Fat_Liquido', orientation='h',
            title=f"Top Produtos - {lab_sel}",
            labels={'Fat_Liquido': 'Faturamento (R$)', 'Produto': ''},
            color='Fat_Liquido', color_continuous_scale='Blues'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=550, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        tabela_prod = prod_stats.copy()
        tabela_prod_export = tabela_prod.copy()
        tabela_prod['Fat_Liquido'] = tabela_prod['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_prod['Quantidade'] = tabela_prod['Quantidade'].apply(lambda x: f"{x:,}")
        st.dataframe(
            tabela_prod[['Produto', 'Num_Clientes', 'Quantidade', 'Fat_Liquido']].rename(columns={'Num_Clientes': 'Clientes'}),
            use_container_width=True, height=500
        )
        gerar_csv_download(tabela_prod_export, f"produtos_{lab_sel}.csv")

    with tab3:
        lab_sel_v = st.selectbox("Selecione o Laboratório:", ['Todos'] + lab_stats['Laboratório'].tolist(), key='lab_vend')

        if lab_sel_v != 'Todos':
            df_lv = df_filtrado[df_filtrado['Fabricante'] == lab_sel_v]
        else:
            df_lv = df_filtrado

        vend_stats = df_lv.groupby('Vendedor').agg({
            'Fat_Liquido_Float': 'sum', 'Quantidade': 'sum', 'Cliente': 'nunique'
        }).reset_index()
        vend_stats.columns = ['Vendedor', 'Fat_Liquido', 'Quantidade', 'Num_Clientes']
        vend_stats = vend_stats.sort_values('Fat_Liquido', ascending=False)

        fig = px.bar(
            vend_stats.head(20), y='Vendedor', x='Fat_Liquido', orientation='h',
            title=f"Vendedores - {lab_sel_v}",
            labels={'Fat_Liquido': 'Faturamento (R$)', 'Vendedor': ''},
            color='Fat_Liquido', color_continuous_scale='Greens'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        tabela_lv = vend_stats.copy()
        tabela_lv_export = tabela_lv.copy()
        tabela_lv['Fat_Liquido'] = tabela_lv['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_lv['Quantidade'] = tabela_lv['Quantidade'].apply(lambda x: f"{x:,}")
        st.dataframe(
            tabela_lv[['Vendedor', 'Num_Clientes', 'Quantidade', 'Fat_Liquido']].rename(columns={'Num_Clientes': 'Clientes'}),
            use_container_width=True, height=500
        )
        gerar_csv_download(tabela_lv_export, f"lab_vendedor_{lab_sel_v}.csv")

    with tab4:
        col_l, col_v = st.columns(2)
        with col_l:
            lab_sel_m = st.selectbox("Laboratório:", lab_stats['Laboratório'].tolist(), key='lab_med')
        with col_v:
            vends = sorted(df_filtrado[df_filtrado['Fabricante'] == lab_sel_m]['Vendedor'].unique().tolist())
            vend_sel_m = st.selectbox("Vendedor:", ['Todos'] + vends, key='vend_med')

        df_med = df_filtrado[df_filtrado['Fabricante'] == lab_sel_m]
        if vend_sel_m != 'Todos':
            df_med = df_med[df_med['Vendedor'] == vend_sel_m]

        med_stats = df_med.groupby(['Produto', 'Vendedor']).agg({
            'Fat_Liquido_Float': 'sum', 'Quantidade': 'sum', 'Cliente': 'nunique'
        }).reset_index()
        med_stats.columns = ['Produto', 'Vendedor', 'Fat_Liquido', 'Quantidade', 'Num_Clientes']
        med_stats = med_stats.sort_values('Fat_Liquido', ascending=False)

        titulo = f"Medicamentos - {lab_sel_m}" + (f" - {vend_sel_m}" if vend_sel_m != 'Todos' else "")
        fig = px.bar(
            med_stats.head(20), y='Produto', x='Fat_Liquido',
            color='Vendedor' if vend_sel_m == 'Todos' else None,
            orientation='h', title=titulo,
            labels={'Fat_Liquido': 'Faturamento (R$)', 'Produto': ''},
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)

        tabela_med = med_stats.copy()
        tabela_med_export = tabela_med.copy()
        tabela_med['Fat_Liquido'] = tabela_med['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_med['Quantidade'] = tabela_med['Quantidade'].apply(lambda x: f"{x:,}")
        st.dataframe(
            tabela_med[['Produto', 'Vendedor', 'Num_Clientes', 'Quantidade', 'Fat_Liquido']].rename(columns={'Num_Clientes': 'Clientes'}),
            use_container_width=True, height=600
        )
        gerar_csv_download(tabela_med_export, f"med_{lab_sel_m}_{vend_sel_m}.csv")


# ========================
# PERFORMANCE VENDEDORES
# ========================
elif visao == "Performance Vendedores":
    st.markdown("## 👤 Performance de Vendedores")

    vend_stats = df_filtrado.groupby('Vendedor').agg({
        'Fat_Liquido_Float': 'sum',
        'Fat_Bruto_Float': 'sum',
        'Cliente': 'nunique',
        'Produto': 'nunique',
        'Fabricante': 'nunique',
        'Quantidade': 'sum'
    }).reset_index()
    vend_stats.columns = ['Vendedor', 'Fat_Liquido', 'Fat_Bruto', 'Num_Clientes', 'Num_Produtos', 'Num_Labs', 'Quantidade']
    vend_stats['Ticket_Medio'] = vend_stats['Fat_Liquido'] / vend_stats['Num_Clientes']
    vend_stats = vend_stats.sort_values('Fat_Liquido', ascending=False)

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 Vendedores", f"{len(vend_stats)}")
    with col2:
        total_v = vend_stats['Fat_Liquido'].sum()
        st.metric("💰 Fat. Total", f"R$ {total_v/1e6:.2f}M")
    with col3:
        media_ticket = vend_stats['Ticket_Medio'].mean()
        st.metric("🎯 Ticket Médio (média)", f"R$ {media_ticket/1e3:.1f}k")

    st.markdown("---")

    tab_v1, tab_v2, tab_v3 = st.tabs(["📊 Comparativo", "📅 Evolução Mensal", "🔍 Detalhamento"])

    with tab_v1:
        st.markdown("### Faturamento por Vendedor")
        fig = px.bar(
            vend_stats, y='Vendedor', x='Fat_Liquido', orientation='h',
            labels={'Fat_Liquido': 'Faturamento (R$)', 'Vendedor': ''},
            color='Fat_Liquido', color_continuous_scale='Viridis'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Clientes por Vendedor")
            fig = px.bar(
                vend_stats, y='Vendedor', x='Num_Clientes', orientation='h',
                labels={'Num_Clientes': 'Clientes', 'Vendedor': ''},
                color='Num_Clientes', color_continuous_scale='Blues'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Ticket Médio por Vendedor")
            fig = px.bar(
                vend_stats, y='Vendedor', x='Ticket_Medio', orientation='h',
                labels={'Ticket_Medio': 'Ticket Médio (R$)', 'Vendedor': ''},
                color='Ticket_Medio', color_continuous_scale='Oranges'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    with tab_v2:
        st.markdown("### Evolução Mensal por Vendedor")
        vend_mensal = df_filtrado.groupby(['Mes_Ano', 'Vendedor'])['Fat_Liquido_Float'].sum().reset_index()
        vend_mensal = vend_mensal.sort_values('Mes_Ano')
        vend_mensal['Mes_Label'] = vend_mensal['Mes_Ano'].apply(
            lambda x: f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][int(x.split('-')[1])-1]}/{x.split('-')[0][-2:]}"
        )

        # Top vendedores para o gráfico
        top_vendedores = vend_stats.head(8)['Vendedor'].tolist()
        vend_mensal_top = vend_mensal[vend_mensal['Vendedor'].isin(top_vendedores)]

        fig = px.line(
            vend_mensal_top, x='Mes_Label', y='Fat_Liquido_Float', color='Vendedor',
            labels={'Fat_Liquido_Float': 'Faturamento (R$)', 'Mes_Label': ''},
            markers=True
        )
        fig.update_layout(height=500, legend=dict(orientation="h", yanchor="bottom", y=-0.3))
        st.plotly_chart(fig, use_container_width=True)

        # Tabela pivot
        st.markdown("### Faturamento Mensal (Tabela)")
        pivot = vend_mensal.pivot_table(
            index='Vendedor', columns='Mes_Ano', values='Fat_Liquido_Float',
            aggfunc='sum', fill_value=0
        )
        pivot['Total'] = pivot.sum(axis=1)
        pivot = pivot.sort_values('Total', ascending=False)

        pivot_display = pivot.copy()
        for col in pivot_display.columns:
            pivot_display[col] = pivot_display[col].apply(lambda x: f"R$ {x:,.0f}")

        st.dataframe(pivot_display, use_container_width=True, height=400)
        gerar_csv_download(pivot.reset_index(), "performance_vendedores_mensal.csv")

    with tab_v3:
        st.markdown("### Tabela Detalhada de Performance")
        tabela_v = vend_stats.copy()
        tabela_v_export = tabela_v.copy()
        tabela_v['Fat_Liquido'] = tabela_v['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_v['Fat_Bruto'] = tabela_v['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_v['Ticket_Medio'] = tabela_v['Ticket_Medio'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_v['Quantidade'] = tabela_v['Quantidade'].apply(lambda x: f"{x:,}")

        st.dataframe(
            tabela_v[['Vendedor', 'Num_Clientes', 'Num_Produtos', 'Num_Labs', 'Quantidade', 'Ticket_Medio', 'Fat_Liquido']].rename(
                columns={'Num_Clientes': 'Clientes', 'Num_Produtos': 'Produtos', 'Num_Labs': 'Labs'}
            ),
            use_container_width=True, height=500
        )
        gerar_csv_download(tabela_v_export, "performance_vendedores.csv")


# ========================
# ANÁLISE DE CONTRATOS
# ========================
elif visao == "Análise de Contratos":
    st.markdown("## 📋 Análise de Contratos")

    df_com = df_filtrado[df_filtrado['PEDIDO DE CONTRATO'] == 'Sim']
    df_sem = df_filtrado[df_filtrado['PEDIDO DE CONTRATO'] != 'Sim']

    fat_com = df_com['Fat_Liquido_Float'].sum()
    fat_sem = df_sem['Fat_Liquido_Float'].sum()
    fat_total = fat_com + fat_sem

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pct_com = (fat_com / fat_total * 100) if fat_total > 0 else 0
        st.metric("📋 Fat. c/ Contrato", f"R$ {fat_com/1e6:.2f}M", f"{pct_com:.1f}%")
    with col2:
        st.metric("📄 Fat. s/ Contrato", f"R$ {fat_sem/1e6:.2f}M", f"{100-pct_com:.1f}%")
    with col3:
        clientes_com = df_com['Cliente'].nunique()
        st.metric("👥 Clientes c/ Contrato", f"{clientes_com}")
    with col4:
        clientes_sem = df_sem['Cliente'].nunique()
        st.metric("👥 Clientes s/ Contrato", f"{clientes_sem}")

    st.markdown("---")

    tab_c1, tab_c2, tab_c3 = st.tabs(["📊 Visão Geral", "🎯 Oportunidades", "📅 Evolução"])

    with tab_c1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Distribuição de Faturamento")
            fig = px.pie(
                values=[fat_com, fat_sem], names=['Com Contrato', 'Sem Contrato'],
                color_discrete_sequence=['#48bb78', '#f56565']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Ticket Médio: Contrato vs Sem Contrato")
            ticket_com = fat_com / len(df_com) if len(df_com) > 0 else 0
            ticket_sem = fat_sem / len(df_sem) if len(df_sem) > 0 else 0
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Com Contrato', 'Sem Contrato'],
                y=[ticket_com, ticket_sem],
                marker_color=['#48bb78', '#f56565'],
                text=[f"R$ {ticket_com:,.0f}", f"R$ {ticket_sem:,.0f}"],
                textposition='outside'
            ))
            fig.update_layout(height=400, yaxis_title="Ticket Médio (R$)")
            st.plotly_chart(fig, use_container_width=True)

        # Top grupos com contrato
        st.markdown("### Top Grupos com Contrato")
        grupo_contrato = df_com.groupby('GRUPO DO CLIENTE').agg({
            'Fat_Liquido_Float': 'sum', 'Cliente': 'nunique'
        }).reset_index()
        grupo_contrato.columns = ['Grupo', 'Fat_Liquido', 'Num_Clientes']
        grupo_contrato = grupo_contrato.sort_values('Fat_Liquido', ascending=False)

        tabela_gc = grupo_contrato.head(20).copy()
        tabela_gc['Fat_Liquido'] = tabela_gc['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(
            tabela_gc.rename(columns={'Num_Clientes': 'Clientes'}),
            use_container_width=True, height=500
        )

    with tab_c2:
        st.markdown("### Clientes de Alto Faturamento SEM Contrato")
        st.caption("Estes clientes têm faturamento significativo mas não possuem contrato - oportunidades de negociação")

        # Clientes sem contrato com alto faturamento
        clientes_sem_contrato = df_sem.groupby(['Cliente', 'GRUPO DO CLIENTE']).agg({
            'Fat_Liquido_Float': 'sum', 'Quantidade': 'sum', 'Produto': 'nunique'
        }).reset_index()
        clientes_sem_contrato.columns = ['Cliente', 'Grupo', 'Fat_Liquido', 'Quantidade', 'Num_Produtos']
        clientes_sem_contrato = clientes_sem_contrato.sort_values('Fat_Liquido', ascending=False)

        # Verificar se cliente também tem contratos (pode ter ambos)
        clientes_com_contrato_set = set(df_com['Cliente'].unique())
        clientes_sem_contrato['Tem_Outros_Contratos'] = clientes_sem_contrato['Cliente'].isin(clientes_com_contrato_set)
        apenas_sem = clientes_sem_contrato[~clientes_sem_contrato['Tem_Outros_Contratos']]

        st.markdown(f"**{len(apenas_sem)} clientes** sem nenhum contrato")

        tabela_opp = apenas_sem.head(30).copy()
        tabela_opp_export = tabela_opp.copy()
        tabela_opp['Fat_Liquido'] = tabela_opp['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_opp['Quantidade'] = tabela_opp['Quantidade'].apply(lambda x: f"{x:,}")

        st.dataframe(
            tabela_opp[['Cliente', 'Grupo', 'Num_Produtos', 'Quantidade', 'Fat_Liquido']].rename(
                columns={'Num_Produtos': 'Produtos'}
            ),
            use_container_width=True, height=600
        )
        gerar_csv_download(tabela_opp_export, "oportunidades_contrato.csv")

    with tab_c3:
        st.markdown("### Evolução Mensal - Contrato vs Sem Contrato")
        mensal_contrato = df_filtrado.groupby(['Mes_Ano', 'PEDIDO DE CONTRATO'])['Fat_Liquido_Float'].sum().reset_index()
        mensal_contrato = mensal_contrato.sort_values('Mes_Ano')
        mensal_contrato['Mes_Label'] = mensal_contrato['Mes_Ano'].apply(
            lambda x: f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][int(x.split('-')[1])-1]}/{x.split('-')[0][-2:]}"
        )
        mensal_contrato['Tipo'] = mensal_contrato['PEDIDO DE CONTRATO'].map({'Sim': 'Com Contrato', 'Não': 'Sem Contrato'})

        fig = px.bar(
            mensal_contrato, x='Mes_Label', y='Fat_Liquido_Float', color='Tipo',
            labels={'Fat_Liquido_Float': 'Faturamento (R$)', 'Mes_Label': ''},
            color_discrete_map={'Com Contrato': '#48bb78', 'Sem Contrato': '#f56565'},
            barmode='group'
        )
        fig.update_layout(height=450, legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)

        # Penetração mensal
        st.markdown("### Taxa de Penetração de Contratos por Mês")
        penetracao = df_filtrado.groupby('Mes_Ano').apply(
            lambda x: (x[x['PEDIDO DE CONTRATO'] == 'Sim']['Fat_Liquido_Float'].sum() / x['Fat_Liquido_Float'].sum() * 100)
            if x['Fat_Liquido_Float'].sum() > 0 else 0
        ).reset_index()
        penetracao.columns = ['Mes_Ano', 'Penetracao']
        penetracao = penetracao.sort_values('Mes_Ano')
        penetracao['Mes_Label'] = penetracao['Mes_Ano'].apply(
            lambda x: f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][int(x.split('-')[1])-1]}/{x.split('-')[0][-2:]}"
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=penetracao['Mes_Label'], y=penetracao['Penetracao'],
            mode='lines+markers+text',
            text=[f"{v:.1f}%" for v in penetracao['Penetracao']],
            textposition='top center',
            line=dict(color='#48bb78', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(height=350, yaxis_title="% do Faturamento com Contrato")
        st.plotly_chart(fig, use_container_width=True)


# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 1.5rem 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.04) 0%, rgba(118, 75, 162, 0.04) 100%);
            border-radius: 12px;'>
    <p style='margin: 0; color: #667eea; font-weight: 600; font-size: 1rem;'>Amoveri Farma</p>
    <p style='margin: 0.3rem 0; color: #4a5568; font-size: 0.85rem;'>Dashboard Comercial</p>
    <p style='margin: 0.3rem 0; color: #718096; font-size: 0.75rem;'>Atualizado: {datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
    <p style='margin: 0.5rem 0 0 0; color: #a0aec0; font-size: 0.7rem;'>Desenvolvido por José Pedro Vieira Silva</p>
</div>
""", unsafe_allow_html=True)
