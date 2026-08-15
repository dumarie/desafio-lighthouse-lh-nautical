import csv
from datetime import datetime, timedelta
from collections import defaultdict

# 1. Ler o arquivo orders.csv e extrair vendas POS e intervalo de datas
vendas_por_data = defaultdict(float)
datas = []

with open('orders.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Verifica canal de venda (pos / loja física)
        channel = row.get('channel', '').strip().lower()
        if channel == 'pos':
            # Extrai apenas a data YYYY-MM-DD
            data_str = row['created_at'].split(' ')[0].split('T')[0]
            dt = datetime.strptime(data_str, '%Y-%m-%d').date()
            total = float(row['total']) if row['total'] else 0.0
            
            vendas_por_data[dt] += total
            datas.append(dt)

data_inicio = min(datas)
data_fim = max(datas)

# 2. Criar Calendário Completo (Dimensão de Datas)
dias_semana_pt = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

faturamento_por_dia_semana = defaultdict(list)
data_atual = data_inicio

while data_atual <= data_fim:
    # Obtém faturamento do dia (se não houver vendas, é 0.0)
    faturamento = vendas_por_data.get(data_atual, 0.0)
    
    # Dia da semana (0 = Segunda-feira, 6 = Domingo no Python)
    num_dia_semana = data_atual.weekday()
    nome_dia_semana = dias_semana_pt[num_dia_semana]
    
    faturamento_por_dia_semana[(num_dia_semana, nome_dia_semana)].append(faturamento)
    data_atual += timedelta(days=1)

# 3. Exibir Resultados
print(f"📅 Período analisado: {data_inicio} até {data_fim}\n")
print("📊 --- MÉDIA REAL DE VENDAS POR DIA DA SEMANA (LOJAS FÍSICAS - POS) ---")
print("-" * 75)
print(f"{'Dia da Semana':<18} | {'Total Dias':<12} | {'Faturamento Total':<20} | {'Média Diária':<15}")
print("-" * 75)

resultados = []
for (num, nome), valores in faturamento_por_dia_semana.items():
    total_dias = len(valores)
    fat_total = sum(valores)
    media = fat_total / total_dias if total_dias > 0 else 0
    resultados.append((num, nome, total_dias, fat_total, media))

# Ordena da pior média para a melhor média
resultados.sort(key=lambda x: x[4])

for num, nome, total_dias, fat_total, media in resultados:
    print(f"{nome:<18} | {total_dias:<12} | R$ {fat_total:>16,.2f} | R$ {media:>12,.2f}")

pior_dia = resultados[0]
print("-" * 75)
print(f"\n⚠️ PIOR DIA DA SEMANA PARA LOJAS FÍSICAS: {pior_dia[1].upper()}")
print(f"👉 Média Real: R$ {pior_dia[4]:,.2f} por dia")