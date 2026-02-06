# Conexão NetSuite - Web Query e Power BI

## Visão Geral

O NetSuite permite exportar dados de Saved Searches via **Web Query (.iqy)** ou conectar diretamente via **Power BI/Power Query**.

---

## 1. Formato do Arquivo .iqy (Web Query)

O arquivo `.iqy` é um arquivo de conexão web do Excel. Estrutura:

```
WEB
1
https://[ACCOUNT_ID].app.netsuite.com/app/reporting/webquery.nl?compid=[ACCOUNT]&entity=[ENTITY_ID]&email=[EMAIL]&role=[ROLE_ID]&cr=[SAVED_SEARCH_ID]&hash=[HASH]

Selection=EntirePage
Formatting=All
PreFormattedTextToColumns=True
ConsecutiveDelimitersAsOne=True
SingleBlockTextImport=False
```

### Parâmetros da URL:

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `compid` | ID da conta NetSuite | 6245503 |
| `entity` | ID da entidade/usuário | 17466 |
| `email` | Email do usuário | jose.vieira@amoverifarma.com |
| `role` | ID do papel/role | 1310 |
| `cr` | ID da Saved Search | 770 |
| `hash` | Hash de autenticação | AAEJ7tMQcN2fWZY... |

---

## 2. Como Usar o Arquivo .iqy

### No Excel:

1. Abra o Excel
2. Vá em **Dados > Obter Dados > De Outras Fontes > Da Web**
3. Ou simplesmente dê **duplo clique** no arquivo `.iqy`
4. Na primeira vez, será solicitado suas credenciais NetSuite
5. Os dados serão importados automaticamente

### Atualização:

- **Manual:** Dados > Atualizar Todos
- **Automática:** Configurar atualização em Dados > Conexões > Propriedades

---

## 3. Conexão Direta do Power BI ao NetSuite

### Opção A: Via ODBC (Recomendado para Produção)

1. **Instalar Driver ODBC do NetSuite:**
   - Baixar de: SuiteAnalytics Connect Driver
   - URL: `https://system.netsuite.com/pages/setup/analytics/connect/sadriverdownload.nl`

2. **Configurar DSN:**
   ```
   Nome: NetSuite_Amoveri
   Server ID: [ACCOUNT_ID]
   Role ID: [ROLE_ID]
   Email: [SEU_EMAIL]
   ```

3. **No Power BI:**
   - Obter Dados > ODBC
   - Selecionar a DSN configurada
   - Inserir credenciais

### Opção B: Via Web (Saved Search)

1. No Power BI Desktop, vá em **Obter Dados > Web**

2. Cole a URL do arquivo .iqy (sem o hash):
   ```
   https://6245503.app.netsuite.com/app/reporting/webquery.nl?compid=6245503&entity=17466&email=[SEU_EMAIL]&role=1310&cr=770
   ```

3. Selecione **Básico** e insira:
   - Usuário: seu email NetSuite
   - Senha: sua senha NetSuite

4. O Power BI vai importar a tabela da Saved Search

### Opção C: Via SuiteAnalytics Connect (Power Query M)

```m
// Power Query M - Conexão NetSuite
let
    Source = Odbc.DataSource(
        "dsn=NetSuite_Amoveri",
        [HierarchicalNavigation=true]
    ),
    // Seleciona a tabela ou view desejada
    Tabela = Source{[Name="TRANSACTION", Kind="Table"]}[Data]
in
    Tabela
```

---

## 4. Saved Searches Disponíveis

Para ver as Saved Searches disponíveis no NetSuite:

1. Vá em **Reports > Saved Searches > All Saved Searches**
2. Ou via URL: `https://[ACCOUNT].app.netsuite.com/app/common/search/searchlist.nl`

### Saved Searches Identificadas no Projeto:

| Nome | ID (cr) | Descrição |
|------|---------|-----------|
| Base Vendas DRE Gerencial | 770 | Dados de vendas para DRE |
| *(adicionar outras conforme descobertas)* | | |

---

## 5. Consultas Power Query no Precificador

Analisando a planilha do precificador, as seguintes consultas Power Query estão configuradas:

### Por Centro de Distribuição:
- `Produtos_Saindo_DF` - Produtos do CD Distrito Federal
- `Produtos_Saindo_RJ` - Produtos do CD Rio de Janeiro
- `Produtos_Saindo_SC` - Produtos do CD Santa Catarina
- `Produtos_Saindo_SP` - Produtos do CD São Paulo
- `Produtos_Fidelize_DF` - Produtos Fidelize
- `Produtos_Hospitalar_DF` - Linha Hospitalar

### Listas:
- `Lista_Medicamentos` - Lista geral de medicamentos
- `Lista_Medicamentos_CEMED` - Lista CMED
- `Lista_Medicamentos_Orgão_Público` - Órgãos públicos

### Por Laboratório (Custo Médio):
- `Accord` - Tabela Accord
- `Biopas` - Tabela Biopas
- `Halex` - Tabela Halex
- `Hypera` - Tabela Hypera
- `Cristália` - Tabela Cristália
- `Sun_Farma` - Tabela Sun Farma
- `União_Química` - Tabela União Química
- `Camber` - Tabela Camber
- `Amoveri` - Tabela Amoveri

---

## 6. Extração dos Dados via Python

Se precisar acessar os dados do NetSuite via Python:

### Opção 1: Download via requests (Web Query)

```python
import requests
from requests_ntlm import HttpNtlmAuth

url = "https://6245503.app.netsuite.com/app/reporting/webquery.nl"
params = {
    "compid": "6245503",
    "entity": "17466",
    "email": "jose.vieira@amoverifarma.com",
    "role": "1310",
    "cr": "770",
    "hash": "SEU_HASH"
}

response = requests.get(url, params=params, auth=('email', 'senha'))
# Os dados vêm em formato HTML/tabela
```

### Opção 2: Via ODBC + pyodbc

```python
import pyodbc

conn_str = (
    "DSN=NetSuite_Amoveri;"
    "UID=seu_email@amoverifarma.com;"
    "PWD=sua_senha"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Executa query
cursor.execute("SELECT * FROM TRANSACTION WHERE ROWNUM <= 100")
rows = cursor.fetchall()
```

---

## 7. Segurança e Boas Práticas

1. **Nunca commitar credenciais** - Use variáveis de ambiente ou arquivo .env
2. **Hash do .iqy expira** - Precisa regenerar periodicamente
3. **Role limitada** - Use role com acesso mínimo necessário
4. **Logs de auditoria** - NetSuite registra todos os acessos

### Exemplo de .env:

```env
NETSUITE_ACCOUNT=6245503
NETSUITE_EMAIL=jose.vieira@amoverifarma.com
NETSUITE_ROLE=1310
NETSUITE_ENTITY=17466
# NÃO armazenar senha ou hash aqui em produção
```

---

## 8. Próximos Passos

1. [ ] Mapear todas as Saved Searches relevantes
2. [ ] Configurar Driver ODBC no servidor/PC
3. [ ] Criar conexão Power BI centralizada
4. [ ] Documentar campos de cada Saved Search
5. [ ] Criar script de atualização automática
