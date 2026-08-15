import csv
from collections import defaultdict

# 1. Carregar Pedidos e Mapear Clientes
orders_by_customer = defaultdict(list)
order_customer_map = {}

with open('orders.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        o_id = row['id']
        c_id = row['customer_id']
        total = float(row['total']) if row['total'] else 0.0
        order_customer_map[o_id] = c_id
        orders_by_customer[c_id].append(total)

# Calcula Frequência e Ticket Médio por cliente
customer_metrics = {}
for c_id, totals in orders_by_customer.items():
    frequencia = len(totals)
    faturamento = sum(totals)
    ticket_medio = faturamento / frequencia if frequencia > 0 else 0
    customer_metrics[c_id] = {
        'frequencia': frequencia,
        'faturamento': faturamento,
        'ticket_medio': ticket_medio
    }

# 2. Carregar Dicionários de Produtos e Categorias
pv_to_p = {}
with open('product_variants.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pv_to_p[row['id']] = row['product_id']

p_to_cat = {}
with open('products.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p_to_cat[row['id']] = row['category_id']

cat_names = {}
with open('categories.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat_names[row['id']] = row['name']

# 3. Mapear Categorias Compradas por Cliente
customer_categories = defaultdict(set)
order_items_list = []

with open('order_items.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        o_id = row['order_id']
        pv_id = row['product_variant_id']
        qty = float(row['quantity']) if row['quantity'] else 0.0
        
        c_id = order_customer_map.get(o_id)
        p_id = pv_to_p.get(pv_id)
        cat_id = p_to_cat.get(p_id)
        
        if c_id and cat_id:
            customer_categories[c_id].add(cat_id)
            order_items_list.append((c_id, cat_id, qty))

# 4. Filtrar Clientes com Diversidade >= 13
eligible_customers = []
for c_id, cats in customer_categories.items():
    if len(cats) >= 13 and c_id in customer_metrics:
        metrics = customer_metrics[c_id]
        eligible_customers.append({
            'customer_id': c_id,
            'ticket_medio': metrics['ticket_medio'],
            'faturamento': metrics['faturamento'],
            'frequencia': metrics['frequencia'],
            'diversidade': len(cats)
        })

# Ordenação: Ticket Médio DESC, customer_id ASC (desempate)
eligible_customers.sort(key=lambda x: (-x['ticket_medio'], int(x['customer_id'])))

top_10 = eligible_customers[:10]
top_10_ids = set(x['customer_id'] for x in top_10)

print("🏆 --- TOP 10 CLIENTES DE ELITE ---")
for idx, c in enumerate(top_10, 1):
    print(f"{idx}º - Cliente ID: {c['customer_id']} | Ticket Médio: R$ {c['ticket_medio']:.2f} | Categorias: {c['diversidade']}")

# 5. Categoria Mais Vendida para o Top 10
category_qty = defaultdict(float)
for c_id, cat_id, qty in order_items_list:
    if c_id in top_10_ids:
        category_qty[cat_id] += qty

print("\n📦 --- CATEGORIA MAIS VENDIDA PARA O TOP 10 ---")
sorted_cats = sorted(category_qty.items(), key=lambda x: x[1], reverse=True)

top_cat_id, top_qty = sorted_cats[0]
top_cat_name = cat_names.get(top_cat_id, 'Desconhecida')

print(f"🥇 Categoria Campeã: {top_cat_name} (ID: {top_cat_id})")
print(f"📊 Total de Itens Comprados: {top_qty:,.0f} unidades")