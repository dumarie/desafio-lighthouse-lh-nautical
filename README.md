# LH Nautical — Relatório Executivo de Analytics & Inteligência Preditiva

> **Projeto desenvolvido como solução para o Desafio Lighthouse (Indicium).**  
> **Autora:** Maria Eduarda Sá (`dumarie`)  
> **Tecnologias:** Python, SQL (PostgreSQL), Looker Studio, Pandas, Scikit-Learn

---

## 📌 Visão Geral do Projeto

Este repositório contém a documentação técnica, scripts SQL/Python e o relatório executivo desenvolvidos para a **LH Nautical**. O objetivo principal do projeto foi diagnosticar a performance de vendas dos canais físicos (POS) e e-commerce, mapear o comportamento dos clientes de elite (VIPs), construir modelos preditivos de demanda e estruturar um algoritmo de recomendação de produtos.

---

## 🎯 Objetivos & Perguntas de Negócio

1. **Desempenho de Lojas Físicas (POS) & Efeito Calendário:** Corrigir a métrica de faturamento médio diário por dia da semana utilizando uma dimensão de datas contínua para evitar distorções provocadas por dias sem vendas.
2. **Mapeamento de Clientes Fiéis (VIPs):** Identificar o Top 10 clientes com maior Ticket Médio que navegam por ampla diversidade do catálogo (13 ou mais categorias) e isolar a categoria com maior volume de itens consumidos por esse grupo.
3. **Previsão de Demanda (Time Series Baseline):** Construir um modelo preditivo baseado em Média Móvel Simples de 3 meses para o produto *Bússola de Bordo 702*, avaliando o Erro Médio Absoluto ($MAE$) e garantindo a ausência de *Data Leakage*.
4. **Sistema de Recomendação de Produtos:** Estruturar uma matriz de co-ocorrência cliente-produto e aplicar a Similaridade de Cosseno para recomendar produtos correlacionados ao *Motor de Popa 1949*.

---

## 🛠️ Metodologia e Tecnologias

* **Linguagens de Programação:** Python (Pandas, NumPy, Scikit-Learn) e SQL (Dialeto PostgreSQL).
* **Banco de Dados Relacional:** PostgreSQL (Modelagem de schema, consultas com CTEs, funções de agregação e cruzamentos de chaves PK/FK).
* **Visualização de Dados:** Looker Studio (Construção de dashboard executivo interativo de 3 páginas).
* **Análise Preditiva & Algoritmos:** Média Móvel (Time Series) e Similaridade de Cosseno (Filtering Collaborative Baseline).

---

## 📊 Principais Resultados & Insights de Negócio

| Frente de Análise | Achado de Negócio | Métrica / Indicador Chave | Recomendação Executiva |
| :--- | :--- | :--- | :--- |
| **Lojas Físicas (POS)** | Quinta-feira é o pior dia de vendas. O Domingo é o 2º pior dia, desmistificando a ideia de alta lucratividade. | Quinta (R$ 157.154,32) vs Domingo (R$ 157.616,13) | Avaliar o custo operacional fixo (escalas/horas extras aos domingos) antes de fechar lojas. |
| **Clientes VIPs** | O Top 10 clientes consome a amplitude máxima do catálogo (14 categorias distintas). | Categoria Campeã VIP: **Hélices (ID 8)** (492 unidades) | Focar em campanhas de *cross-selling* da linha de Hélices para clientes recorrentes. |
| **Previsão de Demanda** | A Média Móvel de 3M sofre com *lag* temporal e não captura picos sazonais de verão. | **$MAE = 16{,}44$ unidades/mês** (Pico de Jan/26: 69 reais vs 25,33 previstos) | Evoluir para modelos com tratamento de sazonalidade (ex: Holt-Winters ou SARIMA). |
| **Recomendação** | Algoritmo identificou forte associação de compra conjunta com itens de propulsão e navegação. | Top Similaridade Válida: *Motor de Popa 5331* (Similaridade: 0.2566) | Implementar motor de recomendação no carrinho para aumentar o Ticket Médio. |

---

## 📁 Estrutura do Repositório

```text
desafio-lighthouse-lh-nautical/
├── csv/                                         # Datasets e bases relacionais brutas (.csv)
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   ├── product_variants.csv
│   ├── customers.csv
│   └── ... (demais tabelas do ERP)
├── dashboard/
│   └── Relatorio_Executivo_LH_Nautical_MariaEduardaSa.pdf  # PDF do Dashboard executivo
├── python/
│   ├── carregar_dados.py                        # Script de carga automatizada dos CSVs para o PostgreSQL
│   ├── gerar_schema.py                          # Criação automatizada da estrutura de tabelas
│   ├── validar_schema.py                        # Validação de integridade e tipos do banco
│   ├── analise_q4.py                            # Diagnóstico em Python para a Q4 (Clientes VIPs)
│   ├── analise_q5.py                            # Diagnóstico em Python para a Q5 (Média POS e Calendário)
│   ├── analise_q6.py                            # Modelo preditivo de Média Móvel 3M e cálculo do MAE
│   ├── analise_q7.py                            # Algoritmo de Similaridade de Cosseno para recomendação
│   ├── executar_q1.py                           # Validação de scripts da etapa 1
│   ├── testar_sql.py                            # Testador de execuções SQL via psycopg2
│   └── contar_linhas.py                         # Script utilitário de auditoria de volumetria
├── sql/
│   ├── schema.sql                               # DDL completo do banco de dados relacional
│   ├── questao4.sql                             # Query da análise de Clientes VIPs e Categorias
│   └── questao5.sql                             # Query da dimensão de calendário e faturamento POS
└── README.md                                    # Documentação oficial do repositório

🚀 Como Executar os Scripts
Pré-requisitos
Python 3.9+

PostgreSQL 12+

Bibliotecas Python: pandas, numpy, psycopg2, scikit-learn

