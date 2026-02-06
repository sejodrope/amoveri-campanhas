"""
Dashboard de Gestão Comercial - NetSuite DRE
Amoveri Farma

Baseado exclusivamente nos dados do NetSuite (DRE Gerencial)
Versão 3.0 - Design Moderno e Elegante

Autor: José Pedro Vieira Silva
Data: 06/02/2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard Comercial - Amoveri Farma",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado para design moderno
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Aplicar fonte em todo o app */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradiente de fundo */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }

    /* Container principal com blur/glass effect */
    .block-container {
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 1rem;
    }

    /* Sidebar moderna */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 1rem;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }

    /* Títulos modernos */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 1.5rem;
    }

    /* Cards de métricas com estilo moderno */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Container de métricas */
    div[data-testid="column"] > div {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }

    div[data-testid="column"] > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(102, 126, 234, 0.2);
    }

    /* Gráficos com bordas arredondadas */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }

    /* Tabelas estilizadas */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }

    /* Botões modernos */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(102, 126, 234, 0.4);
    }

    /* Selectbox e inputs modernos */
    .stSelectbox > div > div,
    .stTextInput > div > div {
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
        background: rgba(102, 126, 234, 0.05);
    }

    /* Separadores */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }

    /* Animação de entrada suave */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .block-container > div {
        animation: fadeIn 0.6s ease-out;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        h1 {
            font-size: 1.8rem;
        }

        h2 {
            font-size: 1.4rem;
        }
    }

    /* Badge/Tag style */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Diretórios
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database" / "campanhas"


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
    """Calcula o trimestre (Q1, Q2, Q3, Q4) a partir da data"""
    try:
        # Formato esperado: DD/MM/YYYY
        data = pd.to_datetime(data_str, format='%d/%m/%Y')
        mes = data.month

        if mes <= 3:
            return 'Q1'
        elif mes <= 6:
            return 'Q2'
        elif mes <= 9:
            return 'Q3'
        else:
            return 'Q4'
    except:
        return 'N/A'


@st.cache_data
def carregar_dre_netsuite():
    """Carrega dados do DRE NetSuite"""
    file_path = DATABASE_DIR / "CTR- BASE VENDAS DRE GERENCIAL - 07.25-02.26.csv"

    # Carregar com skiprows
    df = pd.read_csv(file_path, encoding='utf-8', skiprows=6)
    df.columns = df.columns.str.strip()

    # Criar coluna de valores float
    df['Fat_Bruto_Float'] = df['Faturamento Bruto'].apply(limpar_valor)
    df['Fat_Liquido_Float'] = df['Faturamento Liquido'].apply(limpar_valor)
    df['Desconto_Float'] = df['Valor (desconto)'].apply(limpar_valor)

    # Calcular trimestre
    df['Trimestre'] = df['Data'].apply(calcular_trimestre)

    # Tratamento de campos vazios
    df['UF1'] = df['UF1'].fillna('SEM UF')
    df['GRUPO DO CLIENTE'] = df['GRUPO DO CLIENTE'].fillna('SEM GRUPO')
    df['Parceiro: Representante de vendas'] = df['Parceiro: Representante de vendas'].fillna('SEM PARCEIRO')
    df['Canal de Venda utilizado'] = df['Canal de Venda utilizado'].fillna('SEM CANAL')
    df['PEDIDO DE CONTRATO'] = df['PEDIDO DE CONTRATO'].fillna('Não')

    # Renomear colunas para facilitar
    df = df.rename(columns={
        'Cliente: Tarefa': 'Cliente',
        'Parceiro: Representante de vendas': 'Parceiro',
        'Canal de Venda utilizado': 'Canal',
        'Representante de vendas': 'Vendedor',
        'Item: Nome': 'Produto',
        'Item: Fabricante': 'Fabricante',
        'Categoria de cliente: Nome': 'Categoria',
        'UF1': 'UF'
    })

    return df


# Header com logo e branding
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 💊")
with col2:
    st.title("Dashboard de Gestão Comercial")
    st.markdown("**Amoveri Farma** • v3.0 • NetSuite DRE")

st.markdown("---")

# Sidebar
with st.sidebar:
    # Logo/Branding
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>💊</div>
        <h2 style='margin: 0; font-size: 1.5rem; font-weight: 700;'>Amoveri Farma</h2>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.8;'>Dashboard Comercial</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Carregar dados
    with st.spinner("🔄 Carregando dados..."):
        df = carregar_dre_netsuite()

    # Período
    st.markdown("**📅 Período de Análise**")
    st.success("Jul/2025 - Fev/2026")

    st.markdown("---")

    # Filtros em expander
    with st.expander("🎛️ **Filtros Avançados**", expanded=True):
        st.markdown("**📆 Trimestre**")
        trimestres = ['Todos'] + sorted(df['Trimestre'].unique().tolist())
        trimestre_selecionado = st.selectbox(
            "Trimestre:",
            trimestres,
            label_visibility="collapsed"
        )

        st.markdown("**🗺️ Estado**")
        ufs_disponiveis = ['Todas'] + sorted(df['UF'].unique().tolist())
        uf_selecionada = st.selectbox(
            "UF:",
            ufs_disponiveis,
            label_visibility="collapsed"
        )

        st.markdown("**👤 Parceiro**")
        parceiros = ['Todos'] + sorted(df['Parceiro'].unique().tolist())
        parceiro_selecionado = st.selectbox(
            "Parceiro:",
            parceiros,
            label_visibility="collapsed"
        )

        st.markdown("**📺 Canal**")
        canais = ['Todos'] + sorted(df['Canal'].unique().tolist())
        canal_selecionado = st.selectbox(
            "Canal:",
            canais,
            label_visibility="collapsed"
        )

    st.markdown("---")

    # Visões com ícones
    st.markdown("**📊 Visões Disponíveis**")
    visao = st.radio(
        "Visões:",
        [
            "📈 Visão Geral",
            "🏢 Análise por Grupo",
            "📆 Análise por Trimestre",
            "📺 Análise por Canal",
            "🤝 Análise por Parceiro",
            "🏆 Top Produtos"
        ],
        label_visibility="collapsed"
    )

    # Remover emoji para comparação
    visao = visao.split(" ", 1)[1] if " " in visao else visao

# Aplicar filtros
df_filtrado = df.copy()

if trimestre_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Trimestre'] == trimestre_selecionado]

if uf_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['UF'] == uf_selecionada]

if parceiro_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Parceiro'] == parceiro_selecionado]

if canal_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Canal'] == canal_selecionado]


# ========================
# VISÃO GERAL
# ========================
if visao == "Visão Geral":
    st.markdown("## 📈 Visão Geral do Negócio")

    # KPIs principais
    total_fat_bruto = df_filtrado['Fat_Bruto_Float'].sum()
    total_fat_liquido = df_filtrado['Fat_Liquido_Float'].sum()
    total_desconto = df_filtrado['Desconto_Float'].sum()
    num_transacoes = len(df_filtrado)
    ticket_medio = total_fat_liquido / num_transacoes if num_transacoes > 0 else 0
    taxa_desconto = (total_desconto / total_fat_bruto * 100) if total_fat_bruto > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Faturamento Bruto",
            f"R$ {total_fat_bruto/1e6:.2f}M",
            help="Faturamento bruto total"
        )

    with col2:
        st.metric(
            "💵 Faturamento Líquido",
            f"R$ {total_fat_liquido/1e6:.2f}M",
            help="Faturamento após descontos"
        )

    with col3:
        st.metric(
            "📉 Taxa de Desconto",
            f"{taxa_desconto:.2f}%",
            help="Percentual médio de desconto"
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "📊 Transações",
            f"{num_transacoes:,}",
            help="Número de transações"
        )

    with col5:
        st.metric(
            "🎯 Ticket Médio",
            f"R$ {ticket_medio/1e3:.1f}k",
            help="Ticket médio por transação"
        )

    with col6:
        margem_pct = ((total_fat_liquido / total_fat_bruto) * 100) if total_fat_bruto > 0 else 0
        st.metric(
            "📈 Margem",
            f"{margem_pct:.2f}%",
            help="Margem líquida"
        )

    # Linha adicional com métricas de contratos
    col7, col8, col9 = st.columns(3)

    # Calcular métricas de contratos
    transacoes_com_contrato = df_filtrado[df_filtrado['PEDIDO DE CONTRATO'] == 'Sim']
    num_contratos = len(transacoes_com_contrato)
    pct_contratos = (num_contratos / num_transacoes * 100) if num_transacoes > 0 else 0
    fat_contratos = transacoes_com_contrato['Fat_Liquido_Float'].sum()
    pct_fat_contratos = (fat_contratos / total_fat_liquido * 100) if total_fat_liquido > 0 else 0

    with col7:
        st.metric(
            "📋 Transações com Contrato",
            f"{num_contratos:,}",
            f"{pct_contratos:.1f}% do total",
            help="Transações vinculadas a contratos"
        )

    with col8:
        st.metric(
            "💼 Faturamento via Contratos",
            f"R$ {fat_contratos/1e6:.2f}M",
            f"{pct_fat_contratos:.1f}% do total",
            help="Faturamento de transações com contrato"
        )

    with col9:
        # Clientes únicos em contratos
        clientes_contrato = transacoes_com_contrato['Cliente'].nunique() if num_contratos > 0 else 0
        st.metric(
            "👥 Clientes com Contrato",
            f"{clientes_contrato}",
            help="Clientes únicos com contrato ativo"
        )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📆 Faturamento por Trimestre")
        fat_trimestre = df_filtrado.groupby('Trimestre')['Fat_Liquido_Float'].sum().reset_index()
        fat_trimestre = fat_trimestre.sort_values('Trimestre')

        fig = px.bar(
            fat_trimestre,
            x='Trimestre',
            y='Fat_Liquido_Float',
            title="Faturamento Líquido por Trimestre",
            labels={'Fat_Liquido_Float': 'Faturamento (R$)', 'Trimestre': 'Trimestre'},
            color='Fat_Liquido_Float',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🗺️ Faturamento por UF (Top 10)")
        fat_uf = df_filtrado.groupby('UF')['Fat_Liquido_Float'].sum().reset_index()
        fat_uf = fat_uf.nlargest(10, 'Fat_Liquido_Float')

        fig = px.bar(
            fat_uf,
            x='UF',
            y='Fat_Liquido_Float',
            title="Top 10 UFs",
            labels={'Fat_Liquido_Float': 'Faturamento (R$)', 'UF': 'UF'},
            color='Fat_Liquido_Float',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)


# ========================
# ANÁLISE POR GRUPO
# ========================
elif visao == "Análise por Grupo":
    st.markdown("## 🏢 Análise por Grupo de Cliente")

    # Análise por grupo
    grupo_stats = df_filtrado.groupby('GRUPO DO CLIENTE').agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Desconto_Float': 'sum',
        'Cliente': 'nunique'
    }).reset_index()

    grupo_stats.columns = ['Grupo', 'Fat_Bruto', 'Fat_Liquido', 'Desconto', 'Num_Clientes']
    grupo_stats['Taxa_Desconto'] = (grupo_stats['Desconto'] / grupo_stats['Fat_Bruto'] * 100)
    grupo_stats = grupo_stats.sort_values('Fat_Liquido', ascending=False)

    # KPIs
    num_grupos = len(grupo_stats[grupo_stats['Grupo'] != 'SEM GRUPO'])
    num_sem_grupo = len(df_filtrado[df_filtrado['GRUPO DO CLIENTE'] == 'SEM GRUPO'])
    pct_sem_grupo = (num_sem_grupo / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 Grupos Identificados", f"{num_grupos}")

    with col2:
        st.metric("⚠️ Transações Sem Grupo", f"{num_sem_grupo:,}")

    with col3:
        st.metric("📉 % Sem Grupo", f"{pct_sem_grupo:.1f}%")

    st.markdown("---")

    # Tabela de grupos
    st.markdown("### 🏆 Top 30 Grupos de Clientes")

    top_grupos = grupo_stats.head(30).copy()
    top_grupos['Fat_Bruto'] = top_grupos['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    top_grupos['Fat_Liquido'] = top_grupos['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    top_grupos['Desconto'] = top_grupos['Desconto'].apply(lambda x: f"R$ {x:,.2f}")
    top_grupos['Taxa_Desconto'] = top_grupos['Taxa_Desconto'].apply(lambda x: f"{x:.2f}%")

    st.dataframe(
        top_grupos[['Grupo', 'Num_Clientes', 'Fat_Liquido', 'Fat_Bruto', 'Desconto', 'Taxa_Desconto']],
        use_container_width=True,
        height=600
    )

    # Gráfico
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📊 Top 15 Grupos por Faturamento")
        top15 = grupo_stats.head(15)

        fig = px.bar(
            top15,
            y='Grupo',
            x='Fat_Liquido',
            orientation='h',
            title="Faturamento por Grupo",
            labels={'Fat_Liquido': 'Faturamento Líquido (R$)', 'Grupo': 'Grupo'},
            color='Fat_Liquido',
            color_continuous_scale='Purples'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Concentração")
        total = grupo_stats['Fat_Liquido'].sum()
        top3 = (grupo_stats.head(3)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0
        top5 = (grupo_stats.head(5)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0
        top10 = (grupo_stats.head(10)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0

        st.metric("Top 3 Grupos", f"{top3:.1f}%")
        st.metric("Top 5 Grupos", f"{top5:.1f}%")
        st.metric("Top 10 Grupos", f"{top10:.1f}%")

        if top3 > 40:
            st.warning("🔴 ALTO RISCO: Concentração crítica nos top 3 grupos")
        elif top3 > 30:
            st.warning("🟡 ATENÇÃO: Concentração moderada")
        else:
            st.success("🟢 OK: Boa distribuição")


# ========================
# ANÁLISE POR TRIMESTRE
# ========================
elif visao == "Análise por Trimestre":
    st.markdown("## 📆 Análise Trimestral")

    # Análise por trimestre
    trimestre_stats = df_filtrado.groupby('Trimestre').agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Desconto_Float': 'sum',
        'Cliente': 'nunique'
    }).reset_index()

    trimestre_stats.columns = ['Trimestre', 'Fat_Bruto', 'Fat_Liquido', 'Desconto', 'Num_Clientes']
    trimestre_stats['Taxa_Desconto'] = (trimestre_stats['Desconto'] / trimestre_stats['Fat_Bruto'] * 100)
    trimestre_stats = trimestre_stats.sort_values('Trimestre')

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Evolução Trimestral - Faturamento")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=trimestre_stats['Trimestre'],
            y=trimestre_stats['Fat_Bruto'],
            name='Bruto',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=trimestre_stats['Trimestre'],
            y=trimestre_stats['Fat_Liquido'],
            name='Líquido',
            marker_color='darkblue'
        ))

        fig.update_layout(
            title="Faturamento Bruto vs Líquido por Trimestre",
            xaxis_title="Trimestre",
            yaxis_title="Faturamento (R$)",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📉 Taxa de Desconto por Trimestre")

        fig = px.line(
            trimestre_stats,
            x='Trimestre',
            y='Taxa_Desconto',
            title="Evolução da Taxa de Desconto",
            labels={'Taxa_Desconto': 'Taxa de Desconto (%)', 'Trimestre': 'Trimestre'},
            markers=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Tabela detalhada
    st.markdown("### 📊 Detalhamento Trimestral")

    tabela = trimestre_stats.copy()
    tabela['Fat_Bruto'] = tabela['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Fat_Liquido'] = tabela['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Desconto'] = tabela['Desconto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Taxa_Desconto'] = tabela['Taxa_Desconto'].apply(lambda x: f"{x:.2f}%")

    st.dataframe(tabela, use_container_width=True)


# ========================
# ANÁLISE POR CANAL
# ========================
elif visao == "Análise por Canal":
    st.markdown("## 📺 Análise por Canal de Venda")

    # Análise por canal
    canal_stats = df_filtrado.groupby('Canal').agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Desconto_Float': 'sum',
        'Cliente': 'nunique'
    }).reset_index()

    canal_stats.columns = ['Canal', 'Fat_Bruto', 'Fat_Liquido', 'Desconto', 'Num_Clientes']
    canal_stats['Taxa_Desconto'] = (canal_stats['Desconto'] / canal_stats['Fat_Bruto'] * 100)
    canal_stats['Ticket_Medio'] = canal_stats['Fat_Liquido'] / canal_stats['Num_Clientes']
    canal_stats = canal_stats.sort_values('Fat_Liquido', ascending=False)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Faturamento por Canal")

        fig = px.pie(
            canal_stats.head(10),
            values='Fat_Liquido',
            names='Canal',
            title="Distribuição de Faturamento por Canal (Top 10)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Ticket Médio por Canal")

        top_canais = canal_stats.head(10)
        fig = px.bar(
            top_canais,
            x='Ticket_Medio',
            y='Canal',
            orientation='h',
            title="Ticket Médio por Canal",
            labels={'Ticket_Medio': 'Ticket Médio (R$)', 'Canal': 'Canal'},
            color='Ticket_Medio',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # Tabela
    st.markdown("### 📋 Detalhamento por Canal")

    tabela = canal_stats.copy()
    tabela['Fat_Bruto'] = tabela['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Fat_Liquido'] = tabela['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Desconto'] = tabela['Desconto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Taxa_Desconto'] = tabela['Taxa_Desconto'].apply(lambda x: f"{x:.2f}%")
    tabela['Ticket_Medio'] = tabela['Ticket_Medio'].apply(lambda x: f"R$ {x:,.2f}")

    st.dataframe(
        tabela[['Canal', 'Num_Clientes', 'Fat_Liquido', 'Ticket_Medio', 'Taxa_Desconto']],
        use_container_width=True,
        height=500
    )


# ========================
# ANÁLISE POR PARCEIRO
# ========================
elif visao == "Análise por Parceiro":
    st.markdown("## 🤝 Análise por Parceiro (Representante de Vendas)")

    # Análise por parceiro
    parceiro_stats = df_filtrado.groupby('Parceiro').agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Desconto_Float': 'sum',
        'Cliente': 'nunique'
    }).reset_index()

    parceiro_stats.columns = ['Parceiro', 'Fat_Bruto', 'Fat_Liquido', 'Desconto', 'Num_Clientes']
    parceiro_stats['Taxa_Desconto'] = (parceiro_stats['Desconto'] / parceiro_stats['Fat_Bruto'] * 100)
    parceiro_stats = parceiro_stats.sort_values('Fat_Liquido', ascending=False)

    # KPIs
    col1, col2, col3 = st.columns(3)

    with col1:
        num_parceiros = len(parceiro_stats[parceiro_stats['Parceiro'] != 'SEM PARCEIRO'])
        st.metric("👥 Parceiros Ativos", f"{num_parceiros}")

    with col2:
        total = parceiro_stats['Fat_Liquido'].sum()
        top3 = (parceiro_stats.head(3)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0
        st.metric("🎯 Concentração Top 3", f"{top3:.1f}%")

    with col3:
        taxa_media = parceiro_stats['Taxa_Desconto'].mean()
        st.metric("📉 Taxa Desconto Média", f"{taxa_media:.2f}%")

    st.markdown("---")

    # Gráfico
    st.markdown("### 📊 Top 20 Parceiros por Faturamento")

    top20 = parceiro_stats.head(20)
    fig = px.bar(
        top20,
        y='Parceiro',
        x='Fat_Liquido',
        orientation='h',
        title="Faturamento Líquido por Parceiro",
        labels={'Fat_Liquido': 'Faturamento (R$)', 'Parceiro': 'Parceiro'},
        color='Fat_Liquido',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=700)
    st.plotly_chart(fig, use_container_width=True)

    # Tabela
    st.markdown("### 📋 Detalhamento por Parceiro")

    tabela = parceiro_stats.copy()
    tabela['Fat_Bruto'] = tabela['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Fat_Liquido'] = tabela['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Desconto'] = tabela['Desconto'].apply(lambda x: f"R$ {x:,.2f}")
    tabela['Taxa_Desconto'] = tabela['Taxa_Desconto'].apply(lambda x: f"{x:.2f}%")

    st.dataframe(
        tabela[['Parceiro', 'Num_Clientes', 'Fat_Liquido', 'Fat_Bruto', 'Taxa_Desconto']],
        use_container_width=True,
        height=600
    )


# ========================
# TOP PRODUTOS
# ========================
elif visao == "Top Produtos":
    st.markdown("## 🏆 Análise de Top Produtos")

    # Análise por produto
    produto_stats = df_filtrado.groupby(['Produto', 'Fabricante']).agg({
        'Fat_Bruto_Float': 'sum',
        'Fat_Liquido_Float': 'sum',
        'Quantidade': 'sum'
    }).reset_index()

    produto_stats.columns = ['Produto', 'Fabricante', 'Fat_Bruto', 'Fat_Liquido', 'Quantidade']
    produto_stats = produto_stats.sort_values('Fat_Liquido', ascending=False)

    # Top produtos
    st.markdown("### 🥇 Top 30 Produtos por Faturamento")

    top30 = produto_stats.head(30).copy()
    top30['Fat_Bruto'] = top30['Fat_Bruto'].apply(lambda x: f"R$ {x:,.2f}")
    top30['Fat_Liquido'] = top30['Fat_Liquido'].apply(lambda x: f"R$ {x:,.2f}")
    top30['Quantidade'] = top30['Quantidade'].apply(lambda x: f"{x:,.0f}")

    st.dataframe(
        top30[['Produto', 'Fabricante', 'Quantidade', 'Fat_Liquido', 'Fat_Bruto']],
        use_container_width=True,
        height=600
    )

    # Análise por fabricante
    st.markdown("---")
    st.markdown("### 🏭 Top Fabricantes")

    fabricante_stats = df_filtrado.groupby('Fabricante').agg({
        'Fat_Liquido_Float': 'sum',
        'Produto': 'nunique',
        'Quantidade': 'sum'
    }).reset_index()

    fabricante_stats.columns = ['Fabricante', 'Fat_Liquido', 'Num_Produtos', 'Quantidade']
    fabricante_stats = fabricante_stats.sort_values('Fat_Liquido', ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        top10_fab = fabricante_stats.head(10)

        fig = px.bar(
            top10_fab,
            y='Fabricante',
            x='Fat_Liquido',
            orientation='h',
            title="Top 10 Fabricantes por Faturamento",
            labels={'Fat_Liquido': 'Faturamento (R$)', 'Fabricante': 'Fabricante'},
            color='Fat_Liquido',
            color_continuous_scale='Reds'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Estatísticas")
        num_fabricantes = len(fabricante_stats)
        num_produtos = df_filtrado['Produto'].nunique()

        st.metric("🏭 Fabricantes", f"{num_fabricantes}")
        st.metric("📦 Produtos Únicos", f"{num_produtos}")

        total = fabricante_stats['Fat_Liquido'].sum()
        top5_fab = (fabricante_stats.head(5)['Fat_Liquido'].sum() / total * 100) if total > 0 else 0
        st.metric("🎯 Concentração Top 5", f"{top5_fab:.1f}%")


# Footer elegante
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem 0; margin-top: 3rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            border-radius: 15px;'>
    <p style='margin: 0; color: #667eea; font-weight: 600; font-size: 1.1rem;'>
        💊 Amoveri Farma
    </p>
    <p style='margin: 0.5rem 0; color: #4a5568; font-size: 0.9rem;'>
        Dashboard Comercial v3.0 • NetSuite DRE
    </p>
    <p style='margin: 0.5rem 0; color: #718096; font-size: 0.8rem;'>
        Última atualização: {datetime.now().strftime("%d/%m/%Y às %H:%M")}
    </p>
    <p style='margin: 1rem 0 0 0; color: #a0aec0; font-size: 0.75rem;'>
        Desenvolvido com ❤️ por José Pedro Vieira Silva
    </p>
</div>
""", unsafe_allow_html=True)
