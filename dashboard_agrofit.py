import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# ---------------------------------------------------------
st.set_page_config(page_title="Agrofit Dashboard", layout="wide")
st.title("🌿 Dashboard - Análise de Dados Agrofit")

# Autenticação local com BigQuery
client = bigquery.Client.from_service_account_json("gcp_credentials.json")

# Função utilitária para rodar queries com cache
@st.cache_data(ttl=3600)
def run_query(query):
    return client.query(query).to_dataframe()

# ---------------------------------------------------------
# TABS PRINCIPAIS
# ---------------------------------------------------------
tabs = st.tabs([
    "📈 Visão Geral do Mercado",
    "🏢 Análise de Empresas",
    "🧪 Produtos e Ingredientes",
    "🌍 Geografia e Cadeia de Suprimentos"
])

# ---------------------------------------------------------
# 1️⃣ VISÃO GERAL DO MERCADO
# ---------------------------------------------------------
with tabs[0]:
    st.header("Visão Geral do Mercado de Agrotóxicos")

    # Indicadores principais
    kpis = run_query("""
        SELECT
          COUNT(DISTINCT nr_registro) AS total_produtos,
          COUNT(DISTINCT titular_de_registro) AS total_empresas,
          COUNT(DISTINCT ingrediente_ativo) AS total_ingredientes
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
    """).iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Produtos Registrados", f"{kpis['total_produtos']:,}")
    col2.metric("Empresas Titulares", f"{kpis['total_empresas']:,}")
    col3.metric("Ingredientes Ativos", f"{kpis['total_ingredientes']:,}")

    # Distribuição de produtos por classe
    df_classe = run_query("""
        SELECT classe, COUNT(nr_registro) AS total
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
        GROUP BY classe
        ORDER BY total DESC
    """)
    st.plotly_chart(px.pie(df_classe, names='classe', values='total',
                           title="Distribuição de Produtos por Classe",
                           hole=0.4), use_container_width=True)

    # Perfil de risco ambiental
    df_ambiental = run_query("""
        SELECT classe_ambiental, COUNT(nr_registro) AS total
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
        GROUP BY classe_ambiental
        ORDER BY total DESC
    """)
    st.plotly_chart(px.bar(df_ambiental, x='total', y='classe_ambiental', orientation='h',
                           title="Distribuição por Classe Ambiental",
                           labels={'classe_ambiental':'Classe Ambiental','total':'Total de Produtos'}),
                    use_container_width=True)

# ---------------------------------------------------------
# 2️⃣ ANÁLISE DE EMPRESAS
# ---------------------------------------------------------
with tabs[1]:
    st.header("Análise das Empresas Titulares")

    # Ranking Top 10
    df_empresas = run_query("""
        SELECT titular_de_registro, COUNT(nr_registro) AS total_produtos
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
        GROUP BY titular_de_registro
        ORDER BY total_produtos DESC
        LIMIT 10
    """)
    st.dataframe(df_empresas)
    st.plotly_chart(px.bar(df_empresas, x='titular_de_registro', y='total_produtos',
                           title="Top 10 Empresas por Nº de Produtos",
                           labels={'titular_de_registro':'Empresa','total_produtos':'Produtos'},
                           color='total_produtos'), use_container_width=True)

    # Estratégia de portfólio das top 5
    df_portfolio = run_query("""
        WITH top5 AS (
          SELECT titular_de_registro
          FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
          WHERE SITUACAO = TRUE
          GROUP BY titular_de_registro
          ORDER BY COUNT(nr_registro) DESC
          LIMIT 5
        )
        SELECT t.titular_de_registro, a.classe, COUNT(a.nr_registro) AS total
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv` a
        JOIN top5 t ON a.titular_de_registro = t.titular_de_registro
        WHERE CAST(a.SITUACAO AS STRING) = 'Ativo'
        GROUP BY t.titular_de_registro, a.classe
    """)
    st.plotly_chart(px.bar(df_portfolio, x='titular_de_registro', y='total',
                           color='classe', barmode='relative',
                           title="Especialização de Portfólio das Top 5 Empresas"),
                    use_container_width=True)

# ---------------------------------------------------------
# 3️⃣ ANÁLISE DE PRODUTOS
# ---------------------------------------------------------
with tabs[2]:
    st.header("Análise de Ingredientes e Produtos")

    df_ingredientes = run_query("""
        SELECT ingrediente_ativo, COUNT(nr_registro) AS total
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
        GROUP BY ingrediente_ativo
        ORDER BY total DESC
        LIMIT 30
    """)
    st.plotly_chart(px.bar(df_ingredientes, x='ingrediente_ativo', y='total',
                           title="Principais Ingredientes Ativos",
                           labels={'ingrediente_ativo':'Ingrediente','total':'Frequência'}),
                    use_container_width=True)

    df_heatmap = run_query("""
        SELECT cultura, praga_nome_comum, COUNT(nr_registro) AS total
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
        GROUP BY cultura, praga_nome_comum
        HAVING total > 5
        LIMIT 1000
    """)
    st.plotly_chart(px.density_heatmap(df_heatmap, x='cultura', y='praga_nome_comum', z='total',
                                       title="Concentração de Soluções por Cultura e Praga"),
                    use_container_width=True)

# ---------------------------------------------------------
# 4️⃣ GEOGRAFIA E CADEIA DE SUPRIMENTOS
# ---------------------------------------------------------
with tabs[3]:
    st.header("Análise Geográfica e da Cadeia de Suprimentos")

    df_geo = run_query("""
        SELECT paises, COUNT(DISTINCT titular_de_registro) AS total_empresas
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE AND paises IS NOT NULL
        GROUP BY paises
    """)
    st.plotly_chart(px.choropleth(df_geo, locations='paises', locationmode='country names',
                                  color='total_empresas',
                                  title="Distribuição Geográfica das Empresas"),
                    use_container_width=True)

    df_cadeia = run_query("""
        SELECT tipos, COUNT(nr_registro) AS total
        FROM `authentic-codex-477414-v4.Agrofit_data.tabela_agrofit_csv`
        WHERE SITUACAO = TRUE
        GROUP BY tipos
    """)
    st.plotly_chart(px.bar(df_cadeia, x='tipos', y='total',
                           title="Frequência por Tipo na Cadeia de Produção",
                           labels={'tipos':'Tipo','total':'Total'}),
                    use_container_width=True)
