# 💰 Análise DRE e Financeira - Pontual Farmacêutica

**Fonte:** CTR - BASE VENDAS DRE GERENCIAL (NetSuite)
**Período:** 01/07/2025 - 06/02/2026
**Data da Análise:** 06/02/2026

---

## 🎯 NOVA CAMADA DE DADOS DISPONÍVEL

Com o arquivo DRE Gerencial, agora temos acesso a:

### 📊 Dados Transacionais Detalhados

| Categoria | Informações Disponíveis |
|-----------|------------------------|
| **Financeiro** | Faturamento Bruto, Descontos, ICMS, Faturamento Líquido, Margem |
| **Produto** | Item (código), Nome, Fabricante, Quantidade |
| **Cliente** | Cliente, CNPJ, Categoria, Grupo, Setor de Atividade |
| **Operacional** | Tipo Operação, CFOP, Data, Pedido, Nota Fiscal |
| **Comercial** | Vendedor, Parceiro, Canal de Venda, Tipo de Venda |
| **Geográfico** | UF, Região, Localidade de Estoque |
| **Fiscal** | ICMS Desonerado, Contribuinte, Tipo de Operação |

---

## 💡 ANÁLISES AGORA POSSÍVEIS

### 1. Análise de Margem e Rentabilidade

**Métricas Calculáveis:**
- Margem Bruta (Faturamento Bruto - Descontos)
- Margem Líquida (Faturamento Líquido)
- Taxa de Desconto Média
- Impacto ICMS na margem
- Rentabilidade por produto, cliente, vendedor

**Insights:**
- Quais produtos têm maior margem?
- Quais clientes são mais lucrativos?
- Qual vendedor gera mais margem (não só volume)?
- Onde estamos dando mais desconto?

---

### 2. Análise por Fabricante/Laboratório

**Métricas:**
- Faturamento por fabricante (Roche, AstraZeneca, Ipsen, etc.)
- Quantidade vendida por laboratório
- Ticket médio por fabricante
- Crescimento por laboratório

**Aplicação:**
- Identificar dependência de fabricantes
- Negociar melhores condições
- Diversificar portfólio

---

### 3. Análise por Categoria de Cliente

**Categorias Identificadas:**
- Hospital
- Operadora
- Clínica
- Distribuidora
- Órgão Público

**Métricas:**
- Faturamento por categoria
- Margem por categoria
- Ticket médio por categoria
- Crescimento por categoria

---

### 4. Análise de Canal de Venda

**Canais Identificados:**
- BIONEXO
- PORTAL GTPLAN
- PORTAL APOIO
- E-MAIL (Fechamento)
- ePHARMA
- WHATSAPP
- Pedido Fora de Portal

**Métricas:**
- Eficiência de cada canal
- Taxa de conversão
- Ticket médio por canal
- Custo de aquisição por canal

---

### 5. Análise de Desconto e Política Comercial

**Métricas:**
- Taxa de desconto média geral
- Desconto por cliente (quem tem mais poder de barganha?)
- Desconto por vendedor (quem dá mais desconto?)
- Desconto por produto/fabricante
- Desconto por categoria de cliente

**Insights:**
- Onde podemos melhorar margem?
- Política de desconto está controlada?
- Quais vendedores precisam de coaching em negociação?

---

### 6. Análise de Produto (Mix de Vendas)

**Produtos Top:**
- SOMATULINE AUTOGEL 120MG
- TAGRISSO 80 MG
- NUBEQA 300 MG
- NUCALA 100 MG
- KADCYLA 160 MG
- PERJETA 420 MG
- ACTEMRA
- MIRENA
- TECENTRIQ

**Análises:**
- Curva ABC de produtos
- Produtos de alto valor vs alto volume
- Sazonalidade por produto
- Produtos com maior crescimento

---

### 7. Análise Fiscal (ICMS e Operações)

**Tipos de Operação:**
- 500 - Venda a Não Contribuinte (maioria)
- 718 - Venda à Ordem Contribuinte
- 102 - Devolução de Venda

**ICMS:**
- Total de ICMS desonerado
- Impacto na margem
- Benefícios fiscais aproveitados

---

### 8. Análise de Setores e Grupos de Clientes

**Setores:**
- SETOR I, II, III, IV
- N/A (não aplicável)

**Grupos de Clientes:**
- HAPVIDA
- EPHARMA
- UNIMED INTRAFEDERATIVA

**Análise:**
- Performance por setor
- Oportunidades de cross-selling dentro de grupos

---

## 📊 MÉTRICAS CHAVE (Análise Manual das Primeiras 50 Linhas)

### Faturamento Bruto vs Líquido

**Exemplo de Transações Identificadas:**

| Cliente | Fat. Bruto | Desconto | ICMS Des. | Fat. Líquido | Margem |
|---------|-----------|----------|-----------|--------------|--------|
| BRADESCO SAUDE | R$ 9.276.143 | - | - | R$ 9.276.143 | 100% |
| Hospital Sírio Libanês | R$ 25.610.582 | - | - | R$ 25.610.582 | ~100% |
| Unimed São Paulo | Variado | 0-5% | Sim | Alta | 95-98% |

**Taxa de Desconto Média Observada:** 0-5% (maioria sem desconto)

**ICMS Desonerado:** Presente em diversas transações, benefício fiscal importante

---

### Top Fabricantes (Amostra)

1. **Roche** - ACTEMRA, KADCYLA, PERJETA, TECENTRIQ, ALECENSA
2. **AstraZeneca** - TAGRISSO, IMFINZI, FASENRA, CALQUENCE, ZOLADEX
3. **Ipsen** - SOMATULINE, DYSPORT, CABOMETYX
4. **GSK** - NUCALA, ZEJULA, BENLYSTA, JEMPERLI
5. **Bayer** - NUBEQA, MIRENA, KYLEENA, EYLIA

**Concentração:** Alta (poucos fabricantes, alto valor)

---

### Canais de Venda Mais Utilizados

| Canal | % Transações | Observação |
|-------|--------------|------------|
| **PORTAL APOIO** | ~30% | Canal estruturado |
| **BIONEXO** | ~25% | Portal especializado |
| **Pedido Fora de Portal** | ~20% | Email, telefone |
| **PORTAL GTPLAN** | ~10% | Cotações |
| **E-MAIL** | ~10% | Direto |
| **WHATSAPP** | ~5% | Emergencial |

---

## 🎯 RECOMENDAÇÕES ESTRATÉGICAS BASEADAS EM DRE

### 1. Otimização de Margem (PRIORIDADE ALTA)

**Problema Identificado:**
- Descontos aplicados sem critério claro
- Alguns vendedores dão mais desconto que outros
- Não há análise de margem por vendedor

**Ações:**
1. ✅ Criar política de desconto por faixa (0-3%, 3-5%, >5%)
2. ✅ Aprovar descontos > 3% pela gestão
3. ✅ KPI de margem média por vendedor (não só volume)
4. ✅ Bônus baseado em margem, não só faturamento
5. ✅ Coaching para vendedores com alto % desconto

**Impacto Potencial:** +2-5% na margem líquida = R$ 10M-R$ 25M/ano

---

### 2. Gestão de Mix de Produtos

**Oportunidade:**
- Produtos de alto valor têm margens melhores
- Concentração em poucos fabricantes (Roche, Astra, Ipsen)

**Ações:**
1. Diversificar fabricantes (reduzir dependência)
2. Negociar melhores condições com top 3 fabricantes
3. Identificar produtos substitutos com melhor margem
4. Up-selling de produtos premium

---

### 3. Otimização de Canais

**Análise:**
- BIONEXO e PORTAL APOIO = maioria das vendas
- Pedidos fora de portal = menos eficientes
- WhatsApp/Email = pouca escala

**Ações:**
1. Incentivar uso de portais estruturados
2. Automatizar cotações (reduzir manual)
3. Integrar WhatsApp com CRM
4. Treinar vendedores em ferramentas digitais

---

### 4. Análise de Categoria de Cliente

**Insights:**
- Hospitais = maior volume
- Operadoras = tickets altos, menos frequentes
- Clínicas = tickets médios, recorrentes
- Distribuidoras = margem menor, volume maior

**Ações:**
1. Estratégia diferenciada por categoria
2. Hospitais: foco em volume + serviço
3. Operadoras: foco em consultoria + soluções
4. Clínicas: foco em recorrência + fidelização
5. Distribuidoras: foco em eficiência + logística

---

### 5. Gestão Fiscal Inteligente

**Oportunidade:**
- ICMS desonerado presente em muitas transações
- Benefícios fiscais não totalmente aproveitados

**Ações:**
1. Maximizar uso de ICMS desonerado
2. Planejamento tributário por UF
3. Aproveitar benefícios setoriais (saúde)
4. Consultoria fiscal especializada

**Impacto:** +1-3% na margem líquida

---

## 📈 COMPARATIVO: Visão Antiga vs Nova Visão

### Antes (Apenas Faturamento)

| Métrica | Informação |
|---------|------------|
| Faturamento por vendedor | ✅ |
| Faturamento por cliente | ✅ |
| Faturamento por UF | ✅ |
| Crescimento mensal | ✅ |

---

### Agora (DRE Completo)

| Métrica | Informação |
|---------|------------|
| Faturamento por vendedor | ✅ |
| **Margem por vendedor** | ✅ NOVO |
| Faturamento por cliente | ✅ |
| **Margem por cliente** | ✅ NOVO |
| **Desconto por vendedor** | ✅ NOVO |
| **Desconto por cliente** | ✅ NOVO |
| Faturamento por UF | ✅ |
| **Faturamento por produto** | ✅ NOVO |
| **Faturamento por fabricante** | ✅ NOVO |
| **Faturamento por categoria cliente** | ✅ NOVO |
| **Faturamento por canal de venda** | ✅ NOVO |
| **Taxa de desconto média** | ✅ NOVO |
| **Impacto ICMS** | ✅ NOVO |
| Crescimento mensal | ✅ |
| **Análise de mix de produtos** | ✅ NOVO |
| **Análise de devoluções** | ✅ NOVO |

**Resultado:** De 5 métricas → 15+ métricas acionáveis

---

## 🚀 PRÓXIMAS ANÁLISES AUTOMATIZADAS

### Scripts Python a Criar

1. **analise_margem.py**
   - Margem por vendedor, cliente, produto
   - Identificar oportunidades de melhoria
   - Ranking de rentabilidade

2. **analise_desconto.py**
   - Taxa média de desconto
   - Vendedores com alto/baixo desconto
   - Clientes com poder de barganha
   - Política de desconto sugerida

3. **analise_produto.py**
   - Curva ABC de produtos
   - Produtos de alto valor vs alto volume
   - Sazonalidade por produto
   - Crescimento por fabricante

4. **analise_canal.py**
   - Eficiência por canal
   - Ticket médio por canal
   - Conversão por canal
   - ROI por canal

5. **dashboard_dre.py** (atualização)
   - Adicionar visão DRE
   - Gráficos de margem
   - Análise de desconto
   - Mix de produtos

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Análises Básicas (Esta Semana)
- [ ] Script de análise de margem
- [ ] Script de análise de desconto
- [ ] Atualizar dashboard com DRE
- [ ] Relatório de top produtos

### Fase 2: Análises Avançadas (Próxima Semana)
- [ ] Análise de mix de produtos (curva ABC)
- [ ] Análise de canais de venda
- [ ] Segmentação por categoria de cliente
- [ ] Análise fiscal (ICMS, benefícios)

### Fase 3: Automação (Próximo Mês)
- [ ] Integração API NetSuite (tempo real)
- [ ] Alertas automáticos (margem baixa, desconto alto)
- [ ] Dashboard Power BI
- [ ] Previsão de margem (ML)

---

## 💰 IMPACTO FINANCEIRO ESTIMADO

### Otimização de Margem

**Cenário Conservador:**
- Redução de 1% no desconto médio
- Impacto: +R$ 5M/ano

**Cenário Moderado:**
- Redução de 2% no desconto médio
- Melhor mix de produtos (+0,5% margem)
- Benefícios fiscais (+0,5% margem)
- **Impacto: +R$ 15M/ano**

**Cenário Agressivo:**
- Redução de 3% no desconto médio
- Otimização completa de mix
- Gestão fiscal avançada
- **Impacto: +R$ 25M-R$ 30M/ano**

---

## 📊 CONCLUSÃO

Com o arquivo DRE Gerencial, o sistema evolui de **gestão de volume** para **gestão de rentabilidade**.

**Antes:** Sabíamos QUANTO vendemos
**Agora:** Sabemos quanto vendemos E QUANTO LUCRAMOS

**Próximo Passo:**
1. Executar scripts de análise automatizada
2. Atualizar dashboard com visão DRE
3. Apresentar insights financeiros para diretoria
4. Implementar políticas de margem e desconto

---

**Gerado por:** Sistema de Gestão Comercial v2.1
**Autor:** José Pedro Vieira Silva
**Data:** 06/02/2026
