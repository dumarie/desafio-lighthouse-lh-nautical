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
2. **Mapeamento de Clientes Fiéis (VIPs):** Identificar o Top 10 clientes com maior Ticket Médio que navegam por ampla diversidade do catálogo ($\ge 13$ categorias) e isolar a categoria com maior volume de itens consumidos por esse grupo.
3. **Previsão de Demanda (Time Series Baseline):** Construir um modelo preditivo baseado em Média Móvel Simples de 3 meses para o produto *Bússola de Bordo 702*, avaliando o Erro Médio Absoluto (MAE) e garantindo a ausência de *Data Leakage*.
4. **Sistema de Recomendação de Produtos:** Estruturar uma matriz de co-ocorrência cliente-produto e aplicar a Similaridade de Cosseno para recomendar produtos correlacionados ao *Motor de Popa 1949*.

---

## 🛠️ Metodologia e Tecnologias

* **Linguagens de Programação:** Python (Pandas, NumPy, Scikit-Learn) e SQL (Dialeto PostgreSQL).
* **Banco de Dados Relacional:** PostgreSQL (Modelagem, consultas com CTEs, funções de agregação e cruzamentos de chaves PK/FK).
* **Visualização de Dados:** Looker Studio (Construção de dashboard executivo interativo de 3 páginas).
* **Análise Preditiva & Algoritmos:** Média Móvel Ponderada/Simples (Time Series) e Similaridade de Cosseno (Collaborative Filtering Baseline).

---

## 📊 Principais Resultados & Insights de Negócio

| Frente de Análise | Achado de Negócio | Métrica / Indicador Chave | Recomendação Executiva |
| :--- | :--- | :--- | :--- |
| **Lojas Físicas (POS)** | Quinta-feira é o pior dia de vendas. O Domingo é o 2º pior dia, desmistificando a ideia de alta lucratividade. | Quinta (R$ 157.154,32) vs Domingo (R$ 157.616,13) | Avaliar o custo operacional fixo (escalas/horas extras aos domingos) antes de fechar lojas. |
| **Clientes VIPs** | O Top 10 clientes consome a amplitude máxima do catálogo (14 categorias distintas). | Categoria Campeã VIP: **Hélices (ID 8)** (492 unidades) | Focar em campanhas de *cross-selling* da linha de Hélices para clientes recorrentes. |
| **Previsão de Demanda** | A Média Móvel de 3M sofre com *lag* temporal e não captura picos sazonais de verão. | **MAE = 16,44 unidades/mês** (Pico de Jan/26: 69 reais vs 25,33 previstos) | Evoluir para modelos com tratamento de sazonalidade (ex: Holt-Winters ou SARIMA). |
| **Recomendação** | Algoritmo identificou forte associação de compra conjunta com itens de propulsão e navegação. | Top Similaridade Válida: *Motor de Popa 5331* (Similaridade: 0.2566) | Implementar motor de recomendação no carrinho para aumentar o Ticket Médio. |

---

## 📁 Estrutura do Repositório

```text
├── csv/                                    # Datasets e bases de dados auxiliares
├── dashboard/
│   └── Relatorio_Executivo_LH_Nautical.pdf  # Relatório visual completo (Looker Studio)
├── python/
│   ├── questao_3_carregamento.py            # Carga automatizada dos arquivos CSV no PostgreSQL
│   ├── questao_6_previsao.py               # Modelo de Média Móvel 3M e cálculo do MAE
│   └── questao_7_recomendacao.py           # Matriz de Similaridade de Cosseno
├── sql/
│   ├── questao_4_clientes_vips.sql          # CTEs para Ticket Médio e Diversidade de Categorias
│   └── questao_5_calendario_pos.sql         # Dimensão de Datas com generate_series e LEFT JOIN
└── README.md                                # Documentação oficial do projeto

🚀 Como Executar os Scripts
Pré-requisitos
Python 3.9+

PostgreSQL 12+

Bibliotecas Python: pandas, numpy, psycopg2, scikit-learn

