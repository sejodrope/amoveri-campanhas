# 🎯 Ajustes Dashboard v3.0 - Foco NetSuite

**Data:** 06/02/2026
**Autor:** José Pedro Vieira Silva
**Reunião com:** Nathália (Gestora Comercial)

---

## 📋 RESUMO DAS MUDANÇAS

Após reunião com a gestão, identificamos ajustes críticos no dashboard para focar **exclusivamente nos dados do NetSuite (DRE Gerencial)**, evitando duplicação de valores e melhorando a qualidade das análises.

---

## ✅ AJUSTES IMPLEMENTADOS

### 1. **Fonte de Dados Única: NetSuite DRE**

**Problema Anterior:**
- Dashboard usava múltiplas fontes (Bionexo, resumos CSV, etc.)
- Possível duplicação de valores
- Dados inconsistentes entre fontes

**Solução Implementada:**
- ✅ **Único arquivo:** `CTR- BASE VENDAS DRE GERENCIAL - 07.25-02.26.csv`
- ✅ 17.124 transações processadas
- ✅ Faturamento Bruto: R$ 514,28M
- ✅ Faturamento Líquido: R$ 506,91M

---

### 2. **Filtro por "Parceiro: Representante de Vendas"**

**Problema Anterior:**
- Usava campo genérico "Parceiro"
- Não diferenciava representante de vendas de outros tipos

**Solução Implementada:**
- ✅ Campo específico: **"Parceiro: Representante de vendas"**
- ✅ 14 parceiros identificados
- ✅ Apenas 8 registros sem parceiro (0,05%)
- ✅ Filtro disponível no sidebar do dashboard

**Parceiros Identificados:**
- 21 LUCAS GUILHERME ZANCANELLA BERALDO
- 14 ANDRÉ- AVOC CONSULTORIA
- 24 SANTANA CONSULTORIA EMPRESARIAL LTDA
- E outros...

---

### 3. **Tratamento de Registros Sem UF**

**Problema Anterior:**
- Registros sem UF (possivelmente da base Bionexo)
- Dados incompletos prejudicavam análise geográfica

**Solução Implementada:**
- ✅ Campo: **UF1** (campo correto do NetSuite)
- ✅ Apenas 6 registros sem UF (0,035%)
- ✅ Registros sem UF marcados como "SEM UF"
- ✅ Análise geográfica limpa e precisa

---

### 4. **Agrupamento por Trimestre (Q1, Q2, Q3, Q4)**

**Problema Anterior:**
- Análise mensal (muito granular)
- Difícil visualizar tendências

**Solução Implementada:**
- ✅ **Divisão Trimestral:**
  - **Q1** (Jan-Mar): 3.158 transações - R$ 93,90M
  - **Q2** (Abr-Jun): Não aplicável (período Jul/25-Fev/26)
  - **Q3** (Jul-Set): 6.086 transações - R$ 177,11M
  - **Q4** (Out-Dez): 7.880 transações - R$ 235,91M

- ✅ Filtro por trimestre no dashboard
- ✅ Gráficos de evolução trimestral
- ✅ Comparação entre trimestres

---

### 5. **Unificação por "GRUPO DO CLIENTE"**

**Problema Anterior:**
- Análise apenas por cliente individual
- Não considerava relacionamento entre empresas de um grupo

**Solução Implementada:**
- ✅ Campo: **"GRUPO DO CLIENTE"**
- ✅ 20 grupos identificados
- ✅ 79,2% dos registros sem grupo (serão corrigidos posteriormente)
- ✅ Visão dedicada: "Análise por Grupo"

**Grupos Identificados (exemplos):**
- HAPVIDA
- EPHARMA
- UNIMED INTRAFEDERATIVA
- Etc.

**Próximos Passos:**
- [ ] Subir carga com grupos para clientes sem classificação
- [ ] Ou editar manualmente via interface
- [ ] Revisar e validar agrupamentos existentes

---

### 6. **Canal de Venda Utilizado (Campo Correto)**

**Problema Anterior:**
- Campo desatualizado ou incorreto
- Análise de canal imprecisa

**Solução Implementada:**
- ✅ Campo: **"Canal de Venda utilizado"**
- ✅ 19 canais identificados
- ✅ 100% dos registros com canal
- ✅ Visão dedicada: "Análise por Canal"

**Canais Identificados:**
- BIONEXO
- PORTAL GTPLAN
- PORTAL APOIO
- E-MAIL (Fechamento)
- WHATSAPP
- Pedido Fora de Portal
- E outros...

**Próximos Passos:**
- [ ] Revisar canais desatualizados
- [ ] Subir carga com correções
- [ ] Ou editar manualmente

---

## 📊 NOVO DASHBOARD: `dashboard_netsuite.py`

### Características

**Arquivo:** `Fervereiro/scripts/dashboard_netsuite.py`

**Fonte de Dados:** Exclusivamente NetSuite DRE

**6 Visões Disponíveis:**

1. **📈 Visão Geral**
   - KPIs principais (Fat. Bruto, Líquido, Taxa Desconto, etc.)
   - Faturamento por trimestre
   - Faturamento por UF

2. **🏢 Análise por Grupo**
   - Top 30 grupos de clientes
   - Concentração de risco
   - Ticket médio por grupo
   - **Alerta:** 79,2% sem grupo (a corrigir)

3. **📆 Análise por Trimestre**
   - Evolução trimestral (Q1, Q3, Q4)
   - Faturamento bruto vs líquido
   - Taxa de desconto por trimestre

4. **📺 Análise por Canal**
   - Distribuição por canal
   - Ticket médio por canal
   - Eficiência de cada canal

5. **🤝 Análise por Parceiro**
   - Top 20 parceiros (rep. vendas)
   - Concentração top 3
   - Taxa de desconto média

6. **🏆 Top Produtos**
   - Top 30 produtos por faturamento
   - Top 10 fabricantes
   - Concentração por fabricante

---

## 🎛️ FILTROS DISPONÍVEIS

O dashboard possui filtros interativos no sidebar:

- ✅ **Trimestre:** Q1, Q3, Q4, Todos
- ✅ **UF:** Todas as UFs + filtro individual
- ✅ **Parceiro (Rep. Vendas):** Todos os 14 parceiros
- ✅ **Canal:** Todos os 19 canais

**Filtros são combinados** - você pode selecionar múltiplos critérios simultaneamente.

---

## 🚀 COMO EXECUTAR O NOVO DASHBOARD

### 1. Instalar Dependências (se ainda não fez)

```bash
cd "c:\Users\jose.vieira\OneDrive - GRUPO PONTUAL\Documentos\Amoveri Group\Farma\Campanhas\amoveri-campanhas\Fervereiro\scripts"
pip install -r requirements.txt
```

### 2. Executar Dashboard NetSuite

```bash
python -m streamlit run dashboard_netsuite.py
```

### 3. Acessar no Navegador

O dashboard abrirá automaticamente em: `http://localhost:8501`

---

## 📈 MÉTRICAS PRINCIPAIS DO DASHBOARD

### Faturamento

| Métrica | Valor |
|---------|-------|
| **Faturamento Bruto** | R$ 514,28M |
| **Faturamento Líquido** | R$ 506,91M |
| **Desconto Total** | R$ 7,37M |
| **Taxa de Desconto Média** | 1,43% |
| **Margem Líquida** | 98,57% |

### Transações

| Métrica | Valor |
|---------|-------|
| **Total de Transações** | 17.124 |
| **Ticket Médio** | R$ 29,6k |
| **Clientes Únicos** | ~678 |
| **Produtos Únicos** | ~1.000+ |

### Distribuição Trimestral

| Trimestre | Transações | Faturamento Líquido | % Total |
|-----------|------------|---------------------|---------|
| **Q1** (Jan-Fev/26) | 3.158 | R$ 93,90M | 18,5% |
| **Q3** (Jul-Set/25) | 6.086 | R$ 177,11M | 34,9% |
| **Q4** (Out-Dez/25) | 7.880 | R$ 235,91M | 46,5% |

---

## ⚠️ PONTOS DE ATENÇÃO E PRÓXIMAS AÇÕES

### 1. Grupos de Clientes (PRIORIDADE ALTA)

**Situação:**
- 79,2% dos registros sem grupo
- Apenas 20 grupos identificados
- Análise de grupo limitada

**Ações Necessárias:**
- [ ] Subir carga com mapeamento de clientes → grupos
- [ ] Ou criar interface para classificação manual
- [ ] Validar grupos existentes
- [ ] Estabelecer governança de grupos

**Prazo Sugerido:** 1-2 semanas

---

### 2. Canal de Venda (PRIORIDADE MÉDIA)

**Situação:**
- 100% com canal (ótimo!)
- Alguns canais podem estar desatualizados
- Necessita revisão de nomenclatura

**Ações Necessárias:**
- [ ] Revisar lista de canais
- [ ] Padronizar nomenclatura
- [ ] Atualizar canais desatualizados
- [ ] Documentar política de classificação

**Prazo Sugerido:** 2-3 semanas

---

### 3. UFs Vazias (PRIORIDADE BAIXA)

**Situação:**
- Apenas 6 registros sem UF (0,035%)
- Impacto mínimo nas análises

**Ações Necessárias:**
- [ ] Investigar 6 registros sem UF
- [ ] Corrigir manualmente se necessário

**Prazo Sugerido:** Quando possível

---

## 📊 COMPARATIVO: Dashboard v2.1 vs v3.0

| Aspecto | v2.1 (Anterior) | v3.0 (NetSuite) |
|---------|-----------------|-----------------|
| **Fonte de Dados** | Múltiplas (Bionexo, CSVs) | NetSuite DRE (única) |
| **Transações** | ~20k+ (com duplicações?) | 17.124 (limpo) |
| **Faturamento** | ~R$ 970M | R$ 506,91M (correto) |
| **Parceiro** | Campo genérico | "Parceiro: Rep. Vendas" |
| **UF** | Vários vazios | 0,035% vazios |
| **Trimestre** | ❌ Não havia | ✅ Q1, Q3, Q4 |
| **Grupo Cliente** | ❌ Não havia | ✅ 20 grupos |
| **Canal** | Campo desatualizado | "Canal Venda utilizado" |

---

## 🎯 BENEFÍCIOS DO DASHBOARD v3.0

### 1. **Dados Confiáveis**
- Fonte única (NetSuite)
- Sem duplicações
- Faturamento correto

### 2. **Análise Trimestral**
- Melhor visão de tendências
- Comparação entre períodos
- Planejamento trimestral facilitado

### 3. **Visão por Grupo**
- Análise consolidada de grupos empresariais
- Identificação de relacionamentos
- Estratégias por grupo

### 4. **Canal Correto**
- Análise precisa de eficiência
- ROI por canal
- Otimização de investimentos

### 5. **Parceiro Específico**
- Performance por representante de vendas
- Gestão de comissionamento
- Coaching direcionado

---

## 📝 RECOMENDAÇÕES PARA GESTÃO

### Curto Prazo (1-2 semanas)

1. ✅ **Usar exclusivamente dashboard v3.0 (NetSuite)**
2. ✅ **Iniciar mapeamento de Grupos de Clientes**
3. ✅ **Treinar equipe no novo dashboard**
4. ✅ **Estabelecer governança de dados**

### Médio Prazo (1-2 meses)

1. **Completar classificação de grupos** (objetivo: <10% sem grupo)
2. **Revisar e padronizar canais de venda**
3. **Criar relatórios trimestrais automatizados**
4. **Integrar com metas trimestrais**

### Longo Prazo (3-6 meses)

1. **Integração API NetSuite em tempo real**
2. **Dashboard Power BI corporativo**
3. **Previsão trimestral com ML**
4. **Automatização de alertas**

---

## 🔗 ARQUIVOS RELACIONADOS

### Scripts

- `dashboard_netsuite.py` - **Dashboard principal v3.0** ⭐
- `dashboard.py` - Dashboard antigo v2.1 (deprecado)
- `analise_simples.py` - Análise CLI (mantido para referência)

### Documentação

- `README-PROJETO-ATUALIZADO.md` - Visão geral do projeto
- `07-analise-dre-financeira.md` - Análise DRE detalhada
- `08-AJUSTES-DASHBOARD-NETSUITE.md` - **Este documento**

### Dados

- `CTR- BASE VENDAS DRE GERENCIAL - 07.25-02.26.csv` - **Fonte única** ⭐
- Outros CSVs - Deprecados (manter para histórico)

---

## ✅ CHECKLIST DE TRANSIÇÃO

### Para o Time Comercial

- [ ] Acessar e explorar dashboard v3.0
- [ ] Familiarizar-se com os 6 tipos de visões
- [ ] Entender filtros e suas combinações
- [ ] Identificar clientes sem grupo para classificação
- [ ] Reportar inconsistências encontradas

### Para TI/Dados

- [ ] Monitorar performance do dashboard
- [ ] Estabelecer rotina de atualização do DRE
- [ ] Criar processo de carga de grupos
- [ ] Implementar validações de qualidade
- [ ] Documentar processos de atualização

### Para Gestão

- [ ] Validar métricas com controladoria
- [ ] Definir metas trimestrais
- [ ] Estabelecer cadência de revisão trimestral
- [ ] Aprovar governança de grupos e canais
- [ ] Comunicar mudanças para stakeholders

---

## 📞 SUPORTE

**Dúvidas ou Problemas:**
- José Pedro Vieira Silva
- Email: jose.vieira@farmapontual.local

**Treinamento:**
- Agendar sessão de 1h para apresentação do dashboard
- Material de treinamento disponível

---

**Gerado por:** Sistema de Gestão Comercial v3.0
**Autor:** José Pedro Vieira Silva
**Data:** 06/02/2026
**Status:** ✅ Implementado e Testado
