# Análise de Dados Agrofit - Produtos Formulados

## Visão Geral

Este projeto tem como objetivo analisar a base de dados pública Agrofit - Produtos Formulados, que contém registros de agrotóxicos autorizados no Brasil. O trabalho envolve o tratamento, enriquecimento e exploração dos dados para gerar insights estratégicos.

## Fonte dos Dados

A base de dados pode ser baixada no seguinte link:
[https://dados.gov.br/dados/conjuntos-dados/sistema-de-agrotoxicos-fitossanitarios-agrofit](https://dados.gov.br/dados/conjuntos-dados/sistema-de-agrotoxicos-fitossanitarios-agrofit)

## Requisitos do Projeto

- **Código em Python:** Para o tratamento e enriquecimento dos dados.
- **Dashboard no Google Looker Studio:** Com visualizações e insights gerados a partir da análise.
- **Apresentação em PowerPoint:** Sintetizando o processo de tratamento de dados e os principais resultados.

## Estrutura do Projeto

- `process_data.py`: Script Python para limpeza e pré-processamento dos dados.
- `analyze_data.py`: Script Python para análise exploratória dos dados e geração de insights.
- `.gemini`: Documentação detalhada do processo de limpeza de dados e insights.

## Como Executar

1.  **Pré-requisitos:** Certifique-se de ter Python 3 e as bibliotecas `pandas` instaladas.
    ```bash
    pip install pandas
    ```
2. **Baixar os dados:** Baixe o arquivo `agrofitprodutosformulados.csv` da seção "Fonte dos Dados" e coloque-o na raiz do projeto.
3.  **Processar os dados:** Execute o script de processamento de dados.
    ```bash
    python3 process_data.py
    ```
    Isso irá gerar o arquivo `agrofit_cleaned.csv`.
4.  **Analisar os dados:** Execute o script de análise de dados para obter insights e sugestões de visualização.
    ```bash
    python3 analyze_data.py
    ```

## Próximos Passos

- Desenvolver o dashboard no Google Looker Studio utilizando o arquivo `agrofit_cleaned.csv`.
- Criar a apresentação em PowerPoint com base nos insights gerados.
