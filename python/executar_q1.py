import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

def analisar_questao_1():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 1. Contagem de colunas
    cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'orders';")
    total_colunas = cursor.fetchone()[0]
    
    # 2. Métricas de linhas, datas e totais
    query_metricas = """
    SELECT 
        COUNT(*),
        MIN(created_at),
        MAX(created_at),
        MIN(total),
        MAX(total),
        AVG(total)
    FROM orders;
    """
    cursor.execute(query_metricas)
    linhas, data_min, data_max, val_min, val_max, val_medio = cursor.fetchone()
    
    print("="*60)
    print("📊 RESPOSTA OFICIAL - QUESTÃO 1 (EDA) E 1.1 (SQL)")
    print("="*60)
    print("\n--- PARTE 1: VISÃO GERAL DA TABELA ORDERS ---")
    print(f"• Quantidade total de linhas:  {linhas:,}")
    print(f"• Quantidade total de colunas: {total_colunas}")
    print(f"• Intervalo de datas:          {data_min} até {data_max}")
    
    print("\n--- PARTE 2: ANÁLISE DE VALORES NUMÉRICOS (COLUNA TOTAL) ---")
    print(f"• Valor Mínimo: R$ {val_min:,.2f}")
    print(f"• Valor Máximo: R$ {val_max:,.2f}")
    print(f"• Valor Médio:  R$ {val_medio:,.2f}")
    print("="*60)
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    analisar_questao_1()