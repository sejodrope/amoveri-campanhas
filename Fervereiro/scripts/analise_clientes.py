"""
Análise Automatizada de Vendas por Cliente
Pontual Farmacêutica - Sistema de Gestão Comercial

Autor: José Pedro Vieira Silva
Data: 06/02/2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# Configurações
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database" / "campanhas"
OUTPUT_DIR = BASE_DIR / "analises" / "automatizadas"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Arquivos de entrada
FILE_CLIENTES = DATABASE_DIR / "Resumo de vendas por cliente - 07.25-02.26.csv"
FILE_VENDEDORES = DATABASE_DIR / "Resumo de vendas por representante de vendas 901 - 07.25-02.26.csv"
FILE_PARCEIROS = DATABASE_DIR / "Resumo de vendas por parceiro - 10.25-02.26.csv"


def limpar_valor(valor_str):
    """Converte string de valor em float"""
    if pd.isna(valor_str) or valor_str == '':
        return 0.0

    # Remove espaços, R$, e substitui vírgula por ponto
    valor = str(valor_str).replace('R$', '').replace('.', '').replace(',', '.').strip()

    # Remove aspas se houver
    valor = valor.replace('"', '')

    try:
        return float(valor)
    except:
        return 0.0


def carregar_dados_clientes():
    """Carrega e limpa dados de clientes"""
    print("📊 Carregando dados de clientes...")

    # Ler CSV
    df = pd.read_csv(FILE_CLIENTES, encoding='latin-1')

    # Limpar dados
    df.columns = df.columns.str.strip()

    # Converter vendas para float
    df['Vendas_Float'] = df['Vendas '].apply(limpar_valor)

    # Remover linhas sem cliente
    df = df[df['Cliente '].notna()].copy()
    df = df[df['Cliente '] != '- Sem Cliente/projeto -'].copy()

    # Limpar UF
    df['UF'] = df['UF '].fillna('SEM UF')

    print(f"✅ {len(df)} clientes carregados")
    print(f"💰 Faturamento total: R$ {df['Vendas_Float'].sum():,.2f}")

    return df


def analise_top_clientes(df, top_n=50):
    """Análise dos top clientes"""
    print(f"\n🏆 Analisando Top {top_n} Clientes...")

    top = df.nlargest(top_n, 'Vendas_Float')[['Cliente ', 'Vendas_Float', 'Representante de vendas ', 'UF']].copy()
    top['% do Total'] = (top['Vendas_Float'] / df['Vendas_Float'].sum()) * 100
    top['Acumulado %'] = top['% do Total'].cumsum()

    # Análise de concentração
    top5_pct = top.head(5)['% do Total'].sum()
    top10_pct = top.head(10)['% do Total'].sum()
    top20_pct = top.head(20)['% do Total'].sum()

    print(f"   Top 5 clientes: {top5_pct:.1f}%")
    print(f"   Top 10 clientes: {top10_pct:.1f}%")
    print(f"   Top 20 clientes: {top20_pct:.1f}%")

    return top, {
        'top5_pct': top5_pct,
        'top10_pct': top10_pct,
        'top20_pct': top20_pct
    }


def analise_por_uf(df):
    """Análise de vendas por UF"""
    print("\n🗺️  Analisando vendas por UF...")

    vendas_uf = df.groupby('UF')['Vendas_Float'].agg(['sum', 'count', 'mean']).reset_index()
    vendas_uf.columns = ['UF', 'Total_Vendas', 'Num_Clientes', 'Ticket_Medio']
    vendas_uf['% do Total'] = (vendas_uf['Total_Vendas'] / vendas_uf['Total_Vendas'].sum()) * 100
    vendas_uf = vendas_uf.sort_values('Total_Vendas', ascending=False)

    print(f"   {len(vendas_uf)} UFs identificadas")
    print(f"   Top 5 UFs:")
    for i, row in vendas_uf.head(5).iterrows():
        print(f"      {row['UF']}: R$ {row['Total_Vendas']:,.2f} ({row['% do Total']:.1f}%) - {int(row['Num_Clientes'])} clientes")

    return vendas_uf


def analise_vendedor_x_cliente(df):
    """Análise de relacionamento vendedor × cliente"""
    print("\n👥 Analisando Vendedor × Cliente...")

    # Vendas por vendedor
    vendas_vendedor = df.groupby('Representante de vendas ')['Vendas_Float'].agg(['sum', 'count', 'mean']).reset_index()
    vendas_vendedor.columns = ['Vendedor', 'Total_Vendas', 'Num_Clientes', 'Ticket_Medio']
    vendas_vendedor = vendas_vendedor.sort_values('Total_Vendas', ascending=False)

    # Remover vendedores sem nome
    vendas_vendedor = vendas_vendedor[vendas_vendedor['Vendedor'].notna()].copy()

    print(f"   {len(vendas_vendedor)} vendedores identificados")
    print(f"   Top 5 vendedores por clientes:")
    for i, row in vendas_vendedor.head(5).iterrows():
        print(f"      {row['Vendedor']}: {int(row['Num_Clientes'])} clientes - R$ {row['Total_Vendas']:,.2f}")

    return vendas_vendedor


def analise_segmentacao_clientes(df):
    """Segmentação de clientes por faixa de faturamento"""
    print("\n📊 Segmentando clientes por faturamento...")

    # Definir faixas
    bins = [0, 10000, 50000, 100000, 500000, 1000000, float('inf')]
    labels = [
        '< R$ 10k (Micro)',
        'R$ 10k-50k (Pequeno)',
        'R$ 50k-100k (Médio)',
        'R$ 100k-500k (Grande)',
        'R$ 500k-1M (Muito Grande)',
        '> R$ 1M (Enterprise)'
    ]

    df['Segmento'] = pd.cut(df['Vendas_Float'], bins=bins, labels=labels)

    segmentacao = df.groupby('Segmento')['Vendas_Float'].agg(['sum', 'count']).reset_index()
    segmentacao.columns = ['Segmento', 'Total_Vendas', 'Num_Clientes']
    segmentacao['% Vendas'] = (segmentacao['Total_Vendas'] / segmentacao['Total_Vendas'].sum()) * 100
    segmentacao['% Clientes'] = (segmentacao['Num_Clientes'] / segmentacao['Num_Clientes'].sum()) * 100

    print("\n   Distribuição:")
    for i, row in segmentacao.iterrows():
        print(f"      {row['Segmento']}: {int(row['Num_Clientes'])} clientes ({row['% Clientes']:.1f}%) - R$ {row['Total_Vendas']:,.2f} ({row['% Vendas']:.1f}%)")

    return segmentacao


def identificar_clientes_chave(df, threshold_pct=0.5):
    """Identifica clientes que representam > X% do faturamento"""
    print(f"\n🔑 Identificando clientes-chave (> {threshold_pct}% do faturamento)...")

    total = df['Vendas_Float'].sum()
    df_sorted = df.sort_values('Vendas_Float', ascending=False).copy()
    df_sorted['% Total'] = (df_sorted['Vendas_Float'] / total) * 100

    clientes_chave = df_sorted[df_sorted['% Total'] >= threshold_pct].copy()

    print(f"   {len(clientes_chave)} clientes representam >{threshold_pct}% cada")
    print(f"   Total desses clientes: R$ {clientes_chave['Vendas_Float'].sum():,.2f} ({clientes_chave['% Total'].sum():.1f}%)")

    return clientes_chave


def gerar_relatorio_markdown(df, top_clientes, concentracao, vendas_uf, vendas_vendedor, segmentacao, clientes_chave):
    """Gera relatório em Markdown"""
    print("\n📝 Gerando relatório Markdown...")

    timestamp = datetime.now().strftime("%d/%02/%Y %H:%M")
    total_clientes = len(df)
    total_faturamento = df['Vendas_Float'].sum()
    ticket_medio = df['Vendas_Float'].mean()

    relatorio = f"""# 🏢 Análise Detalhada de Clientes - Pontual Farmacêutica

**Data da Análise:** {timestamp}
**Período:** Julho/2025 - Fevereiro/2026

---

## 📊 VISÃO GERAL

### Números Consolidados

| Métrica | Valor |
|---------|-------|
| **Total de Clientes Ativos** | {total_clientes:,} |
| **Faturamento Total** | R$ {total_faturamento:,.2f} |
| **Ticket Médio por Cliente** | R$ {ticket_medio:,.2f} |
| **Maior Cliente** | R$ {df['Vendas_Float'].max():,.2f} |
| **Menor Cliente (positivo)** | R$ {df[df['Vendas_Float'] > 0]['Vendas_Float'].min():,.2f} |

---

## 🏆 TOP 20 CLIENTES

| # | Cliente | Vendas | % do Total | Acumulado % | Vendedor | UF |
|---|---------|--------|-----------|-------------|----------|---|
"""

    for i, (idx, row) in enumerate(top_clientes.head(20).iterrows(), 1):
        relatorio += f"| {i} | {row['Cliente '][:50]} | R$ {row['Vendas_Float']:,.2f} | {row['% do Total']:.2f}% | {row['Acumulado %']:.2f}% | {row['Representante de vendas '] if pd.notna(row['Representante de vendas ']) else '-'} | {row['UF']} |\n"

    relatorio += f"""

### 📈 Análise de Concentração

**ALERTA:** Concentração de risco por cliente

| Grupo | % do Faturamento | Risco |
|-------|------------------|-------|
| **Top 5 Clientes** | {concentracao['top5_pct']:.1f}% | {"🔴 CRÍTICO" if concentracao['top5_pct'] > 30 else "🟡 ALTO" if concentracao['top5_pct'] > 20 else "🟢 MODERADO"} |
| **Top 10 Clientes** | {concentracao['top10_pct']:.1f}% | {"🔴 CRÍTICO" if concentracao['top10_pct'] > 50 else "🟡 ALTO" if concentracao['top10_pct'] > 40 else "🟢 MODERADO"} |
| **Top 20 Clientes** | {concentracao['top20_pct']:.1f}% | {"🔴 CRÍTICO" if concentracao['top20_pct'] > 70 else "🟡 ALTO" if concentracao['top20_pct'] > 60 else "🟢 MODERADO"} |

---

## 🗺️ ANÁLISE GEOGRÁFICA (TOP 10 UFs)

| # | UF | Faturamento | % do Total | Clientes | Ticket Médio |
|---|----|-----------  |-----------|----------|--------------|
"""

    for i, (idx, row) in enumerate(vendas_uf.head(10).iterrows(), 1):
        relatorio += f"| {i} | {row['UF']} | R$ {row['Total_Vendas']:,.2f} | {row['% do Total']:.2f}% | {int(row['Num_Clientes'])} | R$ {row['Ticket_Medio']:,.2f} |\n"

    relatorio += f"""

---

## 👥 VENDEDORES × CLIENTES (TOP 10)

| # | Vendedor | Clientes | Faturamento | Ticket Médio |
|---|----------|----------|-------------|--------------|
"""

    for i, (idx, row) in enumerate(vendas_vendedor.head(10).iterrows(), 1):
        relatorio += f"| {i} | {row['Vendedor'][:40]} | {int(row['Num_Clientes'])} | R$ {row['Total_Vendas']:,.2f} | R$ {row['Ticket_Medio']:,.2f} |\n"

    relatorio += f"""

---

## 📊 SEGMENTAÇÃO DE CLIENTES

| Segmento | Clientes | % Clientes | Faturamento | % Faturamento |
|----------|----------|-----------|-------------|---------------|
"""

    for idx, row in segmentacao.iterrows():
        relatorio += f"| {row['Segmento']} | {int(row['Num_Clientes'])} | {row['% Clientes']:.1f}% | R$ {row['Total_Vendas']:,.2f} | {row['% Vendas']:.1f}% |\n"

    relatorio += f"""

### Insights:
- **Regra de Pareto:** {segmentacao.iloc[-2:]['% Clientes'].sum():.1f}% dos clientes (Enterprise + Muito Grande) geram {segmentacao.iloc[-2:]['% Vendas'].sum():.1f}% do faturamento
- **Cauda Longa:** {segmentacao.iloc[:2]['% Clientes'].sum():.1f}% dos clientes (Micro + Pequeno) geram apenas {segmentacao.iloc[:2]['% Vendas'].sum():.1f}% do faturamento

---

## 🔑 CLIENTES-CHAVE (> 0,5% do Faturamento)

**Total:** {len(clientes_chave)} clientes representam {clientes_chave['% Total'].sum():.1f}% do faturamento

| Cliente | Vendas | % Total | Vendedor |
|---------|--------|---------|----------|
"""

    for idx, row in clientes_chave.head(30).iterrows():
        relatorio += f"| {row['Cliente '][:50]} | R$ {row['Vendas_Float']:,.2f} | {row['% Total']:.2f}% | {row['Representante de vendas '] if pd.notna(row['Representante de vendas ']) else '-'} |\n"

    relatorio += f"""

---

## 🎯 RECOMENDAÇÕES ESTRATÉGICAS

### 1. Gestão de Risco de Concentração

**Problema:** {"Top 5 clientes representam " + str(round(concentracao['top5_pct'], 1)) + "% do faturamento"}

**Ações:**
- Criar programa de retenção premium para top 20 clientes
- Diversificar base: meta de reduzir top 10 de {concentracao['top10_pct']:.1f}% para < 40% em 12 meses
- Account manager dedicado para cada cliente > R$ 1M/ano

---

### 2. Expansão Geográfica

**Oportunidade:** {len(vendas_uf)} UFs ativas, mas concentração em top 5

**Ações:**
- Expandir presença em UFs com baixa penetração
- Replicar modelo de sucesso de {vendas_uf.iloc[0]['UF']} em outras regiões

---

### 3. Desenvolvimento de Clientes Médios

**Oportunidade:** {int(segmentacao[segmentacao['Segmento'].str.contains('Médio')]['Num_Clientes'].sum())} clientes médios (R$ 50k-100k)

**Ações:**
- Programa de up-selling para elevar médios para grandes (R$ 100k-500k)
- Meta: 30% dos médios crescerem 2x em 12 meses

---

### 4. Otimização de Cauda Longa

**Problema:** {int(segmentacao[segmentacao['Segmento'].str.contains('Micro')]['Num_Clientes'].sum())} clientes micro (< R$ 10k) geram {segmentacao[segmentacao['Segmento'].str.contains('Micro')]['% Vendas'].sum():.1f}% do faturamento

**Decisão:**
- Manter se forem estratégicos (potencial futuro, marca, etc.)
- Descontinuar se custo de servir > margem

---

**Gerado automaticamente por:** Sistema de Gestão Comercial Pontual Farmacêutica
**Script:** analise_clientes.py
**Autor:** José Pedro Vieira Silva
"""

    # Salvar relatório
    output_file = OUTPUT_DIR / "06-analise-clientes-detalhada.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)

    print(f"✅ Relatório salvo em: {output_file}")

    return output_file


def main():
    """Função principal"""
    print("="*60)
    print("📊 ANÁLISE AUTOMATIZADA DE CLIENTES")
    print("Pontual Farmacêutica - Sistema de Gestão Comercial")
    print("="*60)

    # Carregar dados
    df_clientes = carregar_dados_clientes()

    # Análises
    top_clientes, concentracao = analise_top_clientes(df_clientes, top_n=50)
    vendas_uf = analise_por_uf(df_clientes)
    vendas_vendedor = analise_vendedor_x_cliente(df_clientes)
    segmentacao = analise_segmentacao_clientes(df_clientes)
    clientes_chave = identificar_clientes_chave(df_clientes, threshold_pct=0.5)

    # Gerar relatório
    relatorio_file = gerar_relatorio_markdown(
        df_clientes, top_clientes, concentracao, vendas_uf,
        vendas_vendedor, segmentacao, clientes_chave
    )

    # Salvar dados processados para dashboard
    print("\n💾 Salvando dados processados...")

    # Excel com múltiplas abas
    excel_file = OUTPUT_DIR / "dados_clientes_processados.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        top_clientes.to_excel(writer, sheet_name='Top 50 Clientes', index=False)
        vendas_uf.to_excel(writer, sheet_name='Por UF', index=False)
        vendas_vendedor.to_excel(writer, sheet_name='Por Vendedor', index=False)
        segmentacao.to_excel(writer, sheet_name='Segmentação', index=False)
        clientes_chave.to_excel(writer, sheet_name='Clientes-Chave', index=False)

    print(f"✅ Dados salvos em: {excel_file}")

    print("\n" + "="*60)
    print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print(f"\n📄 Relatório: {relatorio_file}")
    print(f"📊 Excel: {excel_file}")
    print(f"\n🚀 Próximo passo: Executar dashboard.py para visualização interativa")


if __name__ == "__main__":
    main()
