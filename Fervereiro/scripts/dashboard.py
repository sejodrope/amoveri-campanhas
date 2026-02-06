"""
Dashboard Interativo de Gestão Comercial
Pontual Farmacêutica

Execute com: streamlit run dashboard.py

Autor: José Pedro Vieira Silva
Data: 06/02/2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard Comercial - Pontual Farmacêutica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diretórios
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database" / "campanhas"


# Funções de carregamento
@st.cache_data
def limpar_valor(valor_str):
    """Converte string de valor em float"""
    if pd.isna(valor_str) or valor_str == '':
        return 0.0
    valor = str(valor_str).replace('R$', '').replace('.', '').replace(',', '.').replace('"', '').strip()
    try:
        return float(valor)
    except:
        return 0.0


@st.cache_data
def carregar_clientes():
    """Carrega dados de clientes"""
    file_path = DATABASE_DIR / "Resumo de vendas por cliente - 07.25-02.26.csv"
    # Skip first 6 rows (header information), row 7 has column names
    # Use UTF-8 encoding to be consistent with parceiros file
    df = pd.read_csv(file_path, encoding='utf-8', skiprows=6)
    df.columns = df.columns.str.strip()
    df['Vendas_Float'] = df['Vendas'].apply(limpar_valor)
    df = df[df['Cliente'].notna()].copy()
    df = df[df['Cliente'] != '- Sem Cliente/projeto -'].copy()
    df['UF'] = df['UF'].fillna('SEM UF')
    return df


@st.cache_data
def carregar_parceiros():
    """Carrega dados de parceiros"""
    file_path = DATABASE_DIR / "Resumo de vendas por parceiro - 10.25-02.26.csv"
    # Skip first 6 rows (header information), row 7 has column names
    # Use UTF-8 encoding to properly handle special characters
    df = pd.read_csv(file_path, encoding='utf-8', skiprows=6)
    df.columns = df.columns.str.strip()

    # Find the transaction column (may have encoding issues with 'ç')
    # It's the second column (index 1)
    col_vendas = df.columns[1]  # Should be 'Total da transação' or similar
    df['Vendas_Float'] = df[col_vendas].apply(limpar_valor)
    return df


# Header
st.title("📊 Dashboard de Gestão Comercial")
st.markdown("### Pontual Farmacêutica - Análise em Tempo Real")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Pontual Farmacêutica")
    st.markdown("---")
    st.markdown("## 🎛️ Filtros")

    # Carregar dados
    with st.spinner("Carregando dados..."):
        df_clientes = carregar_clientes()
        df_parceiros = carregar_parceiros()

    # Filtros
    st.markdown("### 📅 Período")
    st.info("Jul/2025 - Fev/2026")

    st.markdown("### 🗺️ Filtro por UF")
    ufs_disponiveis = ['Todas'] + sorted(df_clientes['UF'].unique().tolist())
    uf_selecionada = st.selectbox("Selecione UF:", ufs_disponiveis)

    st.markdown("### 👤 Filtro por Vendedor")
    vendedores = df_clientes['Representante de vendas'].dropna().unique().tolist()
    vendedor_selecionado = st.selectbox("Selecione Vendedor:", ['Todos'] + sorted(vendedores))

    st.markdown("---")
    st.markdown("### 📊 Visões Disponíveis")
    visao = st.radio(
        "Escolha:",
        ["Visão Geral", "Top Clientes", "Análise Geográfica", "Segmentação", "Parceiros"]
    )

# Aplicar filtros
df_filtrado = df_clientes.copy()
if uf_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['UF'] == uf_selecionada]
if vendedor_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Representante de vendas'] == vendedor_selecionado]


# ========================
# VISÃO GERAL
# ========================
if visao == "Visão Geral":
    st.markdown("## 📈 Visão Geral do Negócio")

    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)

    total_faturamento = df_filtrado['Vendas_Float'].sum()
    total_clientes = len(df_filtrado)
    ticket_medio = df_filtrado['Vendas_Float'].mean()
    maior_cliente = df_filtrado['Vendas_Float'].max()

    with col1:
        st.metric(
            "💰 Faturamento Total",
            f"R$ {total_faturamento/1e6:.2f}M",
            help="Faturamento consolidado Jul/25 - Fev/26"
        )

    with col2:
        st.metric(
            "🏢 Clientes Ativos",
            f"{total_clientes:,}",
            help="Total de clientes com vendas no período"
        )

    with col3:
        st.metric(
            "📊 Ticket Médio",
            f"R$ {ticket_medio/1e3:.1f}k",
            help="Faturamento médio por cliente"
        )

    with col4:
        st.metric(
            "⭐ Maior Cliente",
            f"R$ {maior_cliente/1e6:.2f}M",
            help="Clientecom maior faturamento"
        )

    st.markdown("---")

    # Gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Top 10 Clientes")
        top10 = df_filtrado.nlargest(10, 'Vendas_Float')
        fig = px.bar(
            top10,
            x='Vendas_Float',
            y='Cliente',
            orientation='h',
            title="Faturamento dos Top 10 Clientes",
            labels={'Vendas_Float': 'Faturamento (R$)', 'Cliente': 'Cliente'},
            color='Vendas_Float',
            color_continuous_scale='Blues'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🗺️ Distribuição por UF (Top 10)")
        vendas_uf = df_filtrado.groupby('UF')['Vendas_Float'].sum().reset_index()
        vendas_uf = vendas_uf.nlargest(10, 'Vendas_Float')
        fig = px.pie(
            vendas_uf,
            values='Vendas_Float',
            names='UF',
            title="Participação por Estado",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Concentração de risco
    st.markdown("### ⚠️ Análise de Concentração de Risco")

    df_sorted = df_filtrado.sort_values('Vendas_Float', ascending=False).copy()
    df_sorted['% Total'] = (df_sorted['Vendas_Float'] / df_sorted['Vendas_Float'].sum()) * 100
    df_sorted['% Acumulado'] = df_sorted['% Total'].cumsum()

    top5 = df_sorted.head(5)['% Total'].sum()
    top10 = df_sorted.head(10)['% Total'].sum()
    top20 = df_sorted.head(20)['% Total'].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        cor = "🔴" if top5 > 30 else "🟡" if top5 > 20 else "🟢"
        st.metric(
            f"{cor} Top 5 Clientes",
            f"{top5:.1f}%",
            help="Concentração nos 5 maiores clientes"
        )

    with col2:
        cor = "🔴" if top10 > 50 else "🟡" if top10 > 40 else "🟢"
        st.metric(
            f"{cor} Top 10 Clientes",
            f"{top10:.1f}%",
            help="Concentração nos 10 maiores clientes"
        )

    with col3:
        cor = "🔴" if top20 > 70 else "🟡" if top20 > 60 else "🟢"
        st.metric(
            f"{cor} Top 20 Clientes",
            f"{top20:.1f}%",
            help="Concentração nos 20 maiores clientes"
        )

    # Curva de concentração
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(df_sorted) + 1)),
        y=df_sorted['% Acumulado'].values,
        mode='lines',
        name='% Acumulado',
        line=dict(color='#0066cc', width=3)
    ))
    fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% (Pareto)")
    fig.update_layout(
        title="Curva de Concentração (Pareto)",
        xaxis_title="Número de Clientes",
        yaxis_title="% Acumulado do Faturamento",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)


# ========================
# TOP CLIENTES
# ========================
elif visao == "Top Clientes":
    st.markdown("## 🏆 Top Clientes")

    # Slider para quantidade
    n_clientes = st.slider("Quantos clientes exibir?", 10, 100, 30, 10)

    top_n = df_filtrado.nlargest(n_clientes, 'Vendas_Float').copy()
    top_n['% Total'] = (top_n['Vendas_Float'] / df_filtrado['Vendas_Float'].sum()) * 100
    top_n['% Acumulado'] = top_n['% Total'].cumsum()

    # Tabela
    st.markdown(f"### 📋 Top {n_clientes} Clientes")

    # Formatar para exibição
    top_display = top_n.copy()
    top_display['Vendas'] = top_display['Vendas_Float'].apply(lambda x: f"R$ {x:,.2f}")
    top_display['% do Total'] = top_display['% Total'].apply(lambda x: f"{x:.2f}%")
    top_display['% Acumulado'] = top_display['% Acumulado'].apply(lambda x: f"{x:.2f}%")

    st.dataframe(
        top_display[['Cliente', 'Vendas', '% do Total', '% Acumulado', 'Representante de vendas', 'UF']],
        use_container_width=True,
        height=600
    )

    # Download
    csv = top_n.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"top_{n_clientes}_clientes.csv",
        mime="text/csv"
    )


# ========================
# ANÁLISE GEOGRÁFICA
# ========================
elif visao == "Análise Geográfica":
    st.markdown("## 🗺️ Análise Geográfica")

    # Vendas por UF
    vendas_uf = df_filtrado.groupby('UF').agg({
        'Vendas_Float': ['sum', 'count', 'mean']
    }).reset_index()

    vendas_uf.columns = ['UF', 'Total_Vendas', 'Num_Clientes', 'Ticket_Medio']
    vendas_uf['% do Total'] = (vendas_uf['Total_Vendas'] / vendas_uf['Total_Vendas'].sum()) * 100
    vendas_uf = vendas_uf.sort_values('Total_Vendas', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💰 Faturamento por UF")
        fig = px.bar(
            vendas_uf.head(15),
            x='UF',
            y='Total_Vendas',
            title="Top 15 UFs por Faturamento",
            labels={'Total_Vendas': 'Faturamento (R$)'},
            color='Total_Vendas',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏢 Número de Clientes por UF")
        fig = px.bar(
            vendas_uf.head(15),
            x='UF',
            y='Num_Clientes',
            title="Top 15 UFs por Número de Clientes",
            labels={'Num_Clientes': 'Número de Clientes'},
            color='Num_Clientes',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tabela
    st.markdown("### 📊 Detalhamento por UF")
    vendas_uf_display = vendas_uf.copy()
    vendas_uf_display['Total_Vendas'] = vendas_uf_display['Total_Vendas'].apply(lambda x: f"R$ {x:,.2f}")
    vendas_uf_display['Ticket_Medio'] = vendas_uf_display['Ticket_Medio'].apply(lambda x: f"R$ {x:,.2f}")
    vendas_uf_display['% do Total'] = vendas_uf_display['% do Total'].apply(lambda x: f"{x:.2f}%")

    st.dataframe(vendas_uf_display, use_container_width=True)


# ========================
# SEGMENTAÇÃO
# ========================
elif visao == "Segmentação":
    st.markdown("## 📊 Segmentação de Clientes")

    # Definir segmentos
    bins = [0, 10000, 50000, 100000, 500000, 1000000, float('inf')]
    labels = [
        '< R$ 10k (Micro)',
        'R$ 10k-50k (Pequeno)',
        'R$ 50k-100k (Médio)',
        'R$ 100k-500k (Grande)',
        'R$ 500k-1M (Muito Grande)',
        '> R$ 1M (Enterprise)'
    ]

    df_seg = df_filtrado.copy()
    df_seg['Segmento'] = pd.cut(df_seg['Vendas_Float'], bins=bins, labels=labels)

    segmentacao = df_seg.groupby('Segmento').agg({
        'Vendas_Float': ['sum', 'count']
    }).reset_index()

    segmentacao.columns = ['Segmento', 'Total_Vendas', 'Num_Clientes']
    segmentacao['% Vendas'] = (segmentacao['Total_Vendas'] / segmentacao['Total_Vendas'].sum()) * 100
    segmentacao['% Clientes'] = (segmentacao['Num_Clientes'] / segmentacao['Num_Clientes'].sum()) * 100

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💰 Distribuição de Faturamento")
        fig = px.pie(
            segmentacao,
            values='Total_Vendas',
            names='Segmento',
            title="% do Faturamento por Segmento",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏢 Distribuição de Clientes")
        fig = px.pie(
            segmentacao,
            values='Num_Clientes',
            names='Segmento',
            title="% de Clientes por Segmento",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # Pareto
    st.markdown("### 📈 Análise de Pareto")
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=segmentacao['Segmento'],
        y=segmentacao['% Clientes'],
        name='% Clientes',
        marker_color='lightblue'
    ))

    fig.add_trace(go.Bar(
        x=segmentacao['Segmento'],
        y=segmentacao['% Vendas'],
        name='% Faturamento',
        marker_color='darkblue'
    ))

    fig.update_layout(
        title="Comparação: % Clientes vs % Faturamento",
        barmode='group',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.markdown("### 💡 Insights")

    enterprise_pct = segmentacao[segmentacao['Segmento'] == '> R$ 1M (Enterprise)']['% Vendas'].values[0]
    enterprise_clientes = segmentacao[segmentacao['Segmento'] == '> R$ 1M (Enterprise)']['% Clientes'].values[0]

    st.info(f"""
    **Regra de Pareto:**
    - {enterprise_clientes:.1f}% dos clientes (Enterprise) geram {enterprise_pct:.1f}% do faturamento
    - Foco nesses clientes é CRÍTICO para o negócio
    """)


# ========================
# PARCEIROS
# ========================
elif visao == "Parceiros":
    st.markdown("## 🤝 Análise de Parceiros")

    # Top parceiros
    top_parceiros = df_parceiros.nlargest(20, 'Vendas_Float')

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📊 Top 20 Parceiros")
        fig = px.bar(
            top_parceiros,
            x='Vendas_Float',
            y='Parceiro',
            orientation='h',
            title="Faturamento por Parceiro",
            labels={'Vendas_Float': 'Faturamento (R$)', 'Parceiro': 'Parceiro'},
            color='Vendas_Float',
            color_continuous_scale='Purples'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Concentração")

        total_parceiros = df_parceiros['Vendas_Float'].sum()
        top3 = (top_parceiros.head(3)['Vendas_Float'].sum() / total_parceiros) * 100
        top5 = (top_parceiros.head(5)['Vendas_Float'].sum() / total_parceiros) * 100
        top10 = (top_parceiros.head(10)['Vendas_Float'].sum() / total_parceiros) * 100

        st.metric("Top 3", f"{top3:.1f}%", delta="🔴 Risco Alto" if top3 > 50 else "🟡 Risco Médio")
        st.metric("Top 5", f"{top5:.1f}%", delta="🔴 Risco Alto" if top5 > 70 else "🟡 Risco Médio")
        st.metric("Top 10", f"{top10:.1f}%")

        st.markdown("---")

        st.markdown("### 📈 Distribuição")
        labels = ['Top 3', 'Top 4-10', 'Outros']
        values = [
            top3,
            top10 - top3,
            100 - top10
        ]

        fig = px.pie(
            values=values,
            names=labels,
            title="Distribuição do Faturamento",
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 Dashboard de Gestão Comercial - Pontual Farmacêutica</p>
    <p>Desenvolvido por: José Pedro Vieira Silva | Data: 06/02/2026</p>
    <p>Sistema de Gestão Comercial v2.0</p>
</div>
""", unsafe_allow_html=True)
