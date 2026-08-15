import csv
from datetime import datetime
from collections import defaultdict

# ------------------------------------------------------------------------------
# 1. PASSO 1: UNIFICAÇÃO DOS DATASETS E FILTRAGEM DO PRODUTO "Bússola de Bordo 702"
# ------------------------------------------------------------------------------
NOME_PRODUTO = "Bússola de Bordo 702"

# 1.1 Localizar o ID do produto
product_id = None
with open('products.csv', mode='r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        if row['name'].strip().lower() == NOME_PRODUTO.lower():
            product_id = row['id']
            break

if not product_id:
    raise ValueError(f"Produto '{NOME_PRODUTO}' não encontrado em products.csv")

# 1.2 Localizar todas as variantes associadas ao produto
variant_ids = set()
with open('product_variants.csv', mode='r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        if row['product_id'] == product_id:
            variant_ids.add(row['id'])

# 1.3 Mapear itens de pedidos para as variantes do produto
order_quantities = defaultdict(float)
with open('order_items.csv', mode='r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        if row['product_variant_id'] in variant_ids:
            order_id = row['order_id']
            qtd = float(row['quantity']) if row['quantity'] else 0.0
            order_quantities[order_id] += qtd

# 1.4 Unir com a data dos pedidos (orders.csv) e agrupar por Mês (YYYY-MM)
vendas_mensais = defaultdict(float)
datas_pedidos = []

with open('orders.csv', mode='r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        order_id = row['id']
        if order_id in order_quantities:
            data_str = row['created_at'].split(' ')[0].split('T')[0]
            dt = datetime.strptime(data_str, '%Y-%m-%d')
            mes_key = dt.strftime('%Y-%m')
            
            vendas_mensais[mes_key] += order_quantities[order_id]
            datas_pedidos.append(dt)

# ------------------------------------------------------------------------------
# 2. PASSO 2: CONSTRUÇÃO DA SÉRIE TEMPORAL CONTÍNUA E DIVISÃO TREINO/TESTE
# ------------------------------------------------------------------------------
min_date = min(datas_pedidos)
max_date = datetime(2026, 3, 31)

# Gerar todos os meses no intervalo
meses = []
cur_year, cur_month = min_date.year, min_date.month
end_year, end_month = max_date.year, max_date.month

while (cur_year, cur_month) <= (end_year, end_month):
    meses.append(f"{cur_year:04d}-{cur_month:02d}")
    cur_month += 1
    if cur_month > 12:
        cur_month = 1
        cur_year += 1

# Garante que meses sem vendas tenham valor 0.0
serie_historica = [vendas_mensais.get(m, 0.0) for m in meses]

# ------------------------------------------------------------------------------
# 3. PASSO 3: MODELO BASELINE (MÉDIA MÓVEL DE 3 MESES) E PREVISÃO Q1 2026
# ------------------------------------------------------------------------------
previsoes = {}
meses_teste = ['2026-01', '2026-02', '2026-03']

for i, m in enumerate(meses):
    if i >= 3:
        # Previsão t baseada nos 3 meses anteriores (t-3, t-2, t-1)
        media_movel_3m = sum(serie_historica[i-3:i]) / 3.0
        previsoes[m] = media_movel_3m

# ------------------------------------------------------------------------------
# 4. PASSO 4: EXIBIÇÃO DOS RESULTADOS E MÉTRICA MAE
# ------------------------------------------------------------------------------
print(f"📦 PRODUTO ANALISADO: {NOME_PRODUTO.upper()}")
print("=" * 70)
print(f"{'Mês/Ano':<12} | {'Venda Real':<15} | {'Previsão (3M)':<18} | {'Erro Absoluto':<15}")
print("-" * 70)

erros_absolutos = []
soma_previsao_q1 = 0.0

for m in meses_teste:
    idx = meses.index(m)
    venda_real = serie_historica[idx]
    prev = previsoes[m]
    erro_abs = abs(venda_real - prev)
    
    erros_absolutos.append(erro_abs)
    soma_previsao_q1 += prev
    
    print(f"{m:<12} | {venda_real:>15,.0f} | {prev:>18,.2f} | {erro_abs:>15,.2f}")

mae = sum(erros_absolutos) / len(erros_absolutos)

print("=" * 70)
print(f"🔮 Soma Total da Previsão para o Q1 2026: {soma_previsao_q1:,.2f} (Arredondado: {round(soma_previsao_q1)})")
print(f"📊 Erro Médio Absoluto (MAE) no Q1 2026  : {mae:,.2f} unidades")
print("=" * 70)