# 🐍 Scripts Python - Sistema de Gestão Comercial

**Pontual Farmacêutica**
**Versão:** 2.0
**Data:** 06/02/2026

---

## 📁 Arquivos Disponíveis

### 1. `analise_clientes.py`
**Descrição:** Análise automatizada de clientes

**Funcionalidades:**
- Análise dos top N clientes
- Concentração de risco (top 5, 10, 20)
- Análise geográfica por UF
- Performance vendedor × cliente
- Segmentação por faixa de faturamento
- Identificação de clientes-chave
- Geração de relatório Markdown automático
- Export para Excel (múltiplas abas)

**Execução:**
```bash
python analise_clientes.py
```

**Output:**
- `analises/automatizadas/06-analise-clientes-detalhada.md` (Relatório)
- `analises/automatizadas/dados_clientes_processados.xlsx` (Dados processados)

---

### 2. `dashboard.py`
**Descrição:** Dashboard interativo web

**Funcionalidades:**
- Visão geral consolidada
- Top clientes (customizável)
- Análise geográfica por UF
- Segmentação de clientes
- Análise de parceiros
- Gráficos interativos
- Filtros por UF e vendedor
- Export de dados

**Execução:**
```bash
streamlit run dashboard.py
```

**Acesso:**
- Navegador abrirá automaticamente em `http://localhost:8501`

**Visões Disponíveis:**
1. **Visão Geral:** KPIs principais, top 10 clientes, distribuição UF, curva de concentração
2. **Top Clientes:** Lista customizável (10-100 clientes), download CSV
3. **Análise Geográfica:** Faturamento e clientes por UF
4. **Segmentação:** Análise de Pareto, distribuição por faixa
5. **Parceiros:** Top 20 parceiros, análise de concentração

---

## 🚀 Instalação

### Passo 1: Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Executar Scripts

**Análise Automatizada:**
```bash
cd scripts
python analise_clientes.py
```

**Dashboard Interativo:**
```bash
cd scripts
streamlit run dashboard.py
```

---

## 📊 Estrutura de Diretórios

```
Fervereiro/
├── scripts/
│   ├── analise_clientes.py       # Script de análise
│   ├── dashboard.py               # Dashboard interativo
│   ├── requirements.txt           # Dependências
│   └── README.md                  # Este arquivo
│
├── database/
│   └── campanhas/
│       ├── Resumo de vendas por cliente - 07.25-02.26.csv
│       ├── Resumo de vendas por representante...csv
│       └── Resumo de vendas por parceiro...csv
│
└── analises/
    └── automatizadas/             # Output dos scripts
        ├── 06-analise-clientes-detalhada.md
        └── dados_clientes_processados.xlsx
```

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
**Solução:** Instale as dependências
```bash
pip install -r requirements.txt
```

### Erro: "FileNotFoundError: [Errno 2] No such file or directory"
**Solução:** Execute o script a partir da pasta correta
```bash
cd c:\Users\jose.vieira\OneDrive - GRUPO PONTUAL\Documentos\Amoveri Group\Farma\Campanhas\amoveri-campanhas\Fervereiro\scripts
python analise_clientes.py
```

### Dashboard não abre no navegador
**Solução:** Abra manualmente: http://localhost:8501

### Encoding error ao ler CSV
**Solução:** O script já usa `encoding='latin-1'`. Se persistir, verifique o arquivo CSV.

---

## 📈 Próximas Features (Roadmap)

### Versão 2.1 (Planejado)
- [ ] Análise de tendências temporais
- [ ] Previsão de vendas (ML)
- [ ] Alertas automáticos (email/Slack)
- [ ] Integração com API NetSuite

### Versão 2.2 (Planejado)
- [ ] Dashboard Power BI
- [ ] App mobile (React Native)
- [ ] Sincronização em tempo real
- [ ] Módulo de CRM integrado

---

## 📞 Suporte

**Desenvolvedor:** José Pedro Vieira Silva
**Email:** [inserir email]
**GitHub:** [inserir repo]

**Gestora Comercial:** Nathália Rodrigues Ramos Mainier

---

## 📝 Changelog

| Versão | Data | Mudanças |
|--------|------|----------|
| 2.0 | 06/02/2026 | ✅ Criação scripts Python |
| | | ✅ Dashboard Streamlit interativo |
| | | ✅ Análise automatizada clientes |
| 1.0 | 06/02/2026 | Documentação manual apenas |

---

## 📄 Licença

**Propriedade:** Pontual Farmacêutica
**Uso:** Interno - Confidencial
**Restrições:** Não distribuir externamente

---

**Última Atualização:** 06/02/2026
