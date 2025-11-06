# 🌿 Agrofit Dashboard - Análise de Dados via BigQuery e Streamlit

## 📊 Visão Geral
Este projeto realiza a análise e visualização interativa da base pública **Agrofit - Produtos Formulados**, disponibilizada pelo Governo Federal do Brasil.  
A proposta faz parte de um **Case Técnico para a vaga de DevOps/DataOps**, com foco em exploração, tratamento e visualização de dados reais no ambiente GCP (Google Cloud Platform).

A nova versão substitui o antigo dashboard em Power BI / Looker Studio por uma **aplicação interativa em Streamlit**, conectada diretamente ao **BigQuery** para consultas dinâmicas e escaláveis.

---

## 🌐 Fonte dos Dados
**Base oficial:** [Agrofit - Produtos Formulados (dados.gov.br)](https://dados.gov.br/dados/conjuntos-dados/sistema-de-agrotoxicos-fitossanitarios-agrofit)  
**Armazenamento:** Google BigQuery  
**Tabela:** `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`

---

## ⚙️ Requisitos do Projeto

- **Python:** 3.10 ou superior  
- **Bibliotecas:**
  ```bash
  pip install streamlit google-cloud-bigquery plotly pandas db-dtypes "numpy<2"
  ```

Credenciais GCP: arquivo gcp_credentials.json com permissões:

- BigQuery Data Viewer
- BigQuery Job User

**Dataset**: authentic-codex-477414-v4.Agrofit_data

## 🧩 Estrutura do Projeto
```
bash
Copiar código
agrofit_dashboard/
│
├── dashboard_agrofit.py      # Aplicação principal Streamlit
├── gcp_credentials.json      # Chave de autenticação da service account
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação principal do projeto
└── project_context.txt       # Histórico técnico e decisões do projeto
```

## 🚀 Como Executar
Clone o projeto:

```bash
Copiar código
git clone <repo_url>
cd agrofit_dashboard
```

### (Opcional) Crie o ambiente virtual:

```bash
Copiar código
python3 -m venv venv
source venv/bin/activate
```

#### Instale as dependências:

```bash
Copiar código
pip install -r requirements.txt
```

#### Certifique-se de que o arquivo gcp_credentials.json está na pasta raiz.

Execute o dashboard:

```bash
Copiar código
streamlit run dashboard_agrofit.py
Acesse no navegador: http://localhost:8501
```

##### Aba	Objetivo	Principais Visualizações
- Visão Geral do Mercado	KPIs gerais e panorama dos registros ativos.	Scorecards, gráfico de pizza (classe), barras (risco ambiental).
- Análise de Empresas	Identificar líderes de mercado e portfólios.	Tabela Top 10, barras empilhadas das Top 5 empresas.
- Produtos e Ingredientes	Explorar a composição técnica e aplicação.	Barras de ingredientes, heatmap de cultura x praga.
- Geografia e Cadeia de Suprimentos	Mapa de origem das empresas e atores.	Mapa coroplético, barras por tipo na cadeia.


## 🔐 Autenticação GCP
O acesso ao BigQuery é realizado via Service Account com credenciais locais:

```python
Copiar código
client = bigquery.Client.from_service_account_json("gcp_credentials.json")
```

### 📄 Como criar a credencial:
Vá para o console IAM do Google Cloud:
[https://console.cloud.google.com/iam-admin/serviceaccounts]

#### Crie uma nova conta de serviço com nome streamlit-dashboard.

Atribua as funções:

- BigQuery Data Viewer
- BigQuery Job User

Gere uma chave JSON, renomeie para gcp_credentials.json e mova para a raiz do projeto.

---

## 🔄 Próximos Passos
- Normalizar campos aninhados do dataset Agrofit (ex: listas de culturas e pragas).
- Implementar camada de limpeza automática no carregamento.
- Adicionar parâmetros dinâmicos (filtros interativos por classe, empresa, país).
- Publicar versão em Streamlit Cloud ou GCP App Engine.

### 🧑‍💻 Autor
Thiago Dias Resende
Desenvolvedor • Analista de Estratégia de Marketing • Professor
Fatec-SP | 5º semestre de Desenvolvimento de Software Multiplataforma

📧 Contato: thiagod.resende15@gmail.com

📅 Última atualização: Novembro / 2025

## 🐳 Executando com Docker

Para facilitar a execução e o deploy, o projeto foi containerizado. Certifique-se de ter o Docker instalado e em execução.

**1. Construa a imagem Docker:**

```bash
docker build -t agrofit-dashboard .
```

**2. Execute o container:**

Substitua `</path/to/your/gcp_credentials.json>` pelo caminho absoluto do seu arquivo de credenciais.

```bash
docker run -p 8501:8501 -v </path/to/your/gcp_credentials.json>:/app/gcp_credentials.json agrofit-dashboard
```

**3. Acesse o dashboard:**

Abra seu navegador e acesse: `http://localhost:8501`
