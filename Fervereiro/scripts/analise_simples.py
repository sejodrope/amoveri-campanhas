"""
Análise Simplificada de Clientes (sem dependências externas)
Pontual Farmacêutica

Autor: José Pedro Vieira Silva
Data: 06/02/2026
"""

import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Configurações
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database" / "campanhas"
OUTPUT_DIR = BASE_DIR / "analises" / "automatizadas"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILE_CLIENTES = DATABASE_DIR / "Resumo de vendas por cliente - 07.25-02.26.csv"


def limpar_valor(valor_str):
    """Converte string de valor em float"""
    if not valor_str or valor_str.strip() == '':
        return 0.0

    # Remove R$, aspas, pontos e substitui vírgula por ponto
    valor = valor_str.replace('R$', '').replace('"', '').replace('.', '').replace(',', '.').strip()

    try:
        return float(valor)
    except:
        return 0.0


def carregar_clientes():
    """Carrega dados de clientes do CSV"""
    print("📊 Carregando dados de clientes...")

    clientes = []

    with open(FILE_CLIENTES, 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cliente = row.get('Cliente ', '').strip()

            if not cliente or cliente == '- Sem Cliente/projeto -':
                continue

            vendas_str = row.get('Vendas ', '0')
            vendas = limpar_valor(vendas_str)

            if vendas == 0:
                continue

            clientes.append({
                'cliente': cliente,
                'vendas': vendas,
                'vendedor': row.get('Representante de vendas ', '').strip(),
                'parceiro': row.get('Parceiro ', '').strip(),
                'uf': row.get('UF ', '').strip() or 'SEM UF'
            })

    print(f"✅ {len(clientes)} clientes carregados")

    total = sum(c['vendas'] for c in clientes)
    print(f"💰 Faturamento total: R$ {total:,.2f}")

    return clientes


def analisar_top_clientes(clientes, n=50):
    """Analisa top N clientes"""
    print(f"\n🏆 Analisando Top {n} Clientes...")

    # Ordenar por vendas
    sorted_clientes = sorted(clientes, key=lambda x: x['vendas'], reverse=True)
    top_n = sorted_clientes[:n]

    # Calcular percentuais
    total = sum(c['vendas'] for c in clientes)

    top_with_pct = []
    acumulado = 0
    for c in top_n:
        pct = (c['vendas'] / total) * 100
        acumulado += pct
        top_with_pct.append({
            **c,
            'pct': pct,
            'acumulado': acumulado
        })

    # Concentração
    top5 = sum(c['pct'] for c in top_with_pct[:5])
    top10 = sum(c['pct'] for c in top_with_pct[:10])
    top20 = sum(c['pct'] for c in top_with_pct[:20])

    print(f"   Top 5 clientes: {top5:.1f}%")
    print(f"   Top 10 clientes: {top10:.1f}%")
    print(f"   Top 20 clientes: {top20:.1f}%")

    return top_with_pct, {'top5': top5, 'top10': top10, 'top20': top20}


def analisar_por_uf(clientes):
    """Analisa vendas por UF"""
    print("\n🗺️  Analisando vendas por UF...")

    uf_data = defaultdict(lambda: {'total': 0, 'count': 0})

    for c in clientes:
        uf = c['uf']
        uf_data[uf]['total'] += c['vendas']
        uf_data[uf]['count'] += 1

    # Converter para lista e ordenar
    uf_list = []
    total_geral = sum(c['vendas'] for c in clientes)

    for uf, data in uf_data.items():
        uf_list.append({
            'uf': uf,
            'total': data['total'],
            'count': data['count'],
            'media': data['total'] / data['count'],
            'pct': (data['total'] / total_geral) * 100
        })

    uf_list.sort(key=lambda x: x['total'], reverse=True)

    print(f"   {len(uf_list)} UFs identificadas")
    print(f"   Top 5 UFs:")
    for uf in uf_list[:5]:
        print(f"      {uf['uf']}: R$ {uf['total']:,.2f} ({uf['pct']:.1f}%) - {uf['count']} clientes")

    return uf_list


def analisar_por_vendedor(clientes):
    """Analisa vendas por vendedor"""
    print("\n👥 Analisando por Vendedor...")

    vendedor_data = defaultdict(lambda: {'total': 0, 'count': 0})

    for c in clientes:
        vendedor = c['vendedor'] or 'SEM VENDEDOR'
        vendedor_data[vendedor]['total'] += c['vendas']
        vendedor_data[vendedor]['count'] += 1

    # Converter para lista e ordenar
    vendedor_list = []
    for vendedor, data in vendedor_data.items():
        vendedor_list.append({
            'vendedor': vendedor,
            'total': data['total'],
            'count': data['count'],
            'media': data['total'] / data['count']
        })

    vendedor_list.sort(key=lambda x: x['total'], reverse=True)

    print(f"   {len(vendedor_list)} vendedores identificados")
    print(f"   Top 5 vendedores:")
    for v in vendedor_list[:5]:
        print(f"      {v['vendedor']}: {v['count']} clientes - R$ {v['total']:,.2f}")

    return vendedor_list


def gerar_relatorio(clientes, top_clientes, concentracao, uf_list, vendedor_list):
    """Gera relatório em Markdown"""
    print("\n📝 Gerando relatório...")

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    total_clientes = len(clientes)
    total_fat = sum(c['vendas'] for c in clientes)
    ticket_medio = total_fat / total_clientes

    relatorio = f"""# 🏢 Análise Detalhada de Clientes - Pontual Farmacêutica

**Data da Análise:** {timestamp}
**Período:** Julho/2025 - Fevereiro/2026

---

## 📊 VISÃO GERAL

| Métrica | Valor |
|---------|-------|
| **Total de Clientes Ativos** | {total_clientes:,} |
| **Faturamento Total** | R$ {total_fat:,.2f} |
| **Ticket Médio por Cliente** | R$ {ticket_medio:,.2f} |

---

## 🏆 TOP 30 CLIENTES

| # | Cliente | Vendas | % Total | Acum % | Vendedor | UF |
|---|---------|--------|---------|--------|----------|---|
"""

    for i, c in enumerate(top_clientes[:30], 1):
        relatorio += f"| {i} | {c['cliente'][:50]} | R$ {c['vendas']:,.2f} | {c['pct']:.2f}% | {c['acumulado']:.2f}% | {c['vendedor'][:30] if c['vendedor'] else '-'} | {c['uf']} |\n"

    relatorio += f"""

### 📈 Análise de Concentração de Risco

| Grupo | % do Faturamento | Status |
|-------|------------------|--------|
| **Top 5 Clientes** | {concentracao['top5']:.1f}% | {"🔴 CRÍTICO" if concentracao['top5'] > 30 else "🟡 ALTO" if concentracao['top5'] > 20 else "🟢 MODERADO"} |
| **Top 10 Clientes** | {concentracao['top10']:.1f}% | {"🔴 CRÍTICO" if concentracao['top10'] > 50 else "🟡 ALTO" if concentracao['top10'] > 40 else "🟢 MODERADO"} |
| **Top 20 Clientes** | {concentracao['top20']:.1f}% | {"🔴 CRÍTICO" if concentracao['top20'] > 70 else "🟡 ALTO" if concentracao['top20'] > 60 else "🟢 MODERADO"} |

---

## 🗺️ TOP 15 UFs

| # | UF | Faturamento | % Total | Clientes | Ticket Médio |
|---|----|-----------  |---------|----------|--------------|
"""

    for i, uf in enumerate(uf_list[:15], 1):
        relatorio += f"| {i} | {uf['uf']} | R$ {uf['total']:,.2f} | {uf['pct']:.2f}% | {uf['count']} | R$ {uf['media']:,.2f} |\n"

    relatorio += f"""

---

## 👥 TOP 15 VENDEDORES

| # | Vendedor | Clientes | Faturamento | Ticket Médio |
|---|----------|----------|-------------|--------------|
"""

    for i, v in enumerate(vendedor_list[:15], 1):
        relatorio += f"| {i} | {v['vendedor'][:40]} | {v['count']} | R$ {v['total']:,.2f} | R$ {v['media']:,.2f} |\n"

    relatorio += f"""

---

## 🎯 RECOMENDAÇÕES ESTRATÉGICAS

### 1. Gestão de Risco - Concentração de Clientes

**Status:** {"🔴 CRÍTICO" if concentracao['top5'] > 30 else "🟡 ATENÇÃO" if concentracao['top5'] > 20 else "🟢 OK"}

**Problema:**
- Top 5 clientes = {concentracao['top5']:.1f}% do faturamento
- Perda de 1 top cliente = impacto severo na receita

**Ações Recomendadas:**
1. ✅ Criar programa de retenção premium para top 20 clientes
2. ✅ Account manager dedicado para cada cliente > R$ 500k/ano
3. ✅ Reuniões trimestrais estratégicas com top 10
4. ✅ Diversificar: meta de reduzir top 10 para < 40% em 12 meses

---

### 2. Expansão Geográfica

**Oportunidade:**
- {len(uf_list)} UFs ativas
- Top 5 UFs = {sum(u['pct'] for u in uf_list[:5]):.1f}% do faturamento

**Ações:**
- Expandir em UFs com baixa penetração mas alto potencial
- Replicar modelo de sucesso de {uf_list[0]['uf']} em outras regiões

---

### 3. Otimização por Vendedor

**Top Performer:** {vendedor_list[0]['vendedor']}
- {vendedor_list[0]['count']} clientes
- R$ {vendedor_list[0]['total']:,.2f} faturamento
- Ticket médio: R$ {vendedor_list[0]['media']:,.2f}

**Ação:**
- Replicar melhores práticas do top performer
- Coaching de vendedores com baixo ticket médio

---

**Gerado por:** analise_simples.py
**Autor:** José Pedro Vieira Silva
**Data:** {timestamp}
"""

    # Salvar
    output_file = OUTPUT_DIR / "06-analise-clientes-detalhada.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)

    print(f"✅ Relatório salvo em: {output_file}")

    return output_file


def main():
    """Função principal"""
    print("="*60)
    print("📊 ANÁLISE SIMPLIFICADA DE CLIENTES")
    print("Pontual Farmacêutica")
    print("="*60)

    # Carregar e analisar
    clientes = carregar_clientes()
    top_clientes, concentracao = analisar_top_clientes(clientes, n=50)
    uf_list = analisar_por_uf(clientes)
    vendedor_list = analisar_por_vendedor(clientes)

    # Gerar relatório
    relatorio_file = gerar_relatorio(clientes, top_clientes, concentracao, uf_list, vendedor_list)

    print("\n" + "="*60)
    print("✅ ANÁLISE CONCLUÍDA!")
    print("="*60)
    print(f"\n📄 Relatório: {relatorio_file}")
    print(f"\n🚀 Para dashboard visual: instale dependências e execute dashboard.py")


if __name__ == "__main__":
    main()
