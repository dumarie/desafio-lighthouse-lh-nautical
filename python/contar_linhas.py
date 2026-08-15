import os

tabelas = ['customers.csv', 'orders.csv', 'order_items.csv', 'payments.csv']
total = 0

print("🔍 Contando linhas dos CSVs brutos:\n")

for arq in tabelas:
    if os.path.exists(arq):
        with open(arq, 'r', encoding='utf-8-sig', errors='replace') as f:
            qtd = sum(1 for _ in f) - 1  # Desconsidera o cabeçalho
            total += qtd
            print(f"• {arq}: {qtd:,} linhas")

print("\n--------------------------------------------------")
print(f"🔥 SOMA TOTAL (Questão 3.2): {total}")
print("--------------------------------------------------")