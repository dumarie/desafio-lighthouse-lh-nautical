import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------------------------------------------------------
# 1. CARGA E PREPARAÇÃO DOS DATASETS (RENOMEANDO 'id' PARA EVITAR CONFLITOS)
# ------------------------------------------------------------------------------
orders = pd.read_csv('orders.csv')[['id', 'customer_id']].rename(columns={'id': 'order_id_orders'})
order_items = pd.read_csv('order_items.csv')
product_variants = pd.read_csv('product_variants.csv')[['id', 'product_id']].rename(columns={'id': 'variant_id_pv'})
products = pd.read_csv('products.csv')[['id', 'name']].rename(columns={'id': 'product_id_prod', 'name': 'product_name'})

# ------------------------------------------------------------------------------
# 2. UNIFICAÇÃO DOS DATASETS
# ------------------------------------------------------------------------------
df = (
    order_items
    .merge(orders, left_on='order_id', right_on='order_id_orders')
    .merge(product_variants, left_on='product_variant_id', right_on='variant_id_pv')
    .merge(products, left_on='product_id', right_on='product_id_prod')
)

# ------------------------------------------------------------------------------
# 3. CONSTRUÇÃO DA MATRIZ DE INTERAÇÃO USUÁRIO x PRODUTO (BINÁRIA)
# ------------------------------------------------------------------------------
# Linhas: customer_id | Colunas: product_name
matriz_interacao = pd.crosstab(df['customer_id'], df['product_name'])

# Regra da Atividade: 1 se comprou ao menos uma vez, 0 caso contrário
matriz_binaria = (matriz_interacao > 0).astype(int)

# ------------------------------------------------------------------------------
# 4. CÁLCULO DA SIMILARIDADE DE COSSENO (PRODUTO x PRODUTO)
# ------------------------------------------------------------------------------
# Transpomos a matriz (.T) para calcular a similaridade entre os produtos
sim_matrix = cosine_similarity(matriz_binaria.T)

# Converter em DataFrame rotulado
sim_df = pd.DataFrame(
    sim_matrix, 
    index=matriz_binaria.columns, 
    columns=matriz_binaria.columns
)

# ------------------------------------------------------------------------------
# 5. RANKING DE SIMILARIDADE PARA "Motor de Popa 1949"
# ------------------------------------------------------------------------------
PRODUTO_ALVO = "Motor de Popa 1949"

if PRODUTO_ALVO in sim_df.columns:
    ranking = (
        sim_df[PRODUTO_ALVO]
        .drop(PRODUTO_ALVO)                # Desconsidera o próprio produto
        .sort_values(ascending=False)      # Ordena do mais similar para o menos
        .head(5)                           # Top 5
    )
    
    print(f"🎯 TOP 5 PRODUTOS MAIS SIMILARES A '{PRODUTO_ALVO.upper()}':\n")
    print("-" * 65)
    print(f"{'Posição':<8} | {'Nome do Produto':<38} | {'Similaridade':<12}")
    print("-" * 65)
    for i, (prod, sim) in enumerate(ranking.items(), 1):
        print(f"{i:<8} | {prod:<38} | {sim:.4f}")
    print("-" * 65)
else:
    print(f"❌ Produto '{PRODUTO_ALVO}' não foi encontrado na base de dados.")