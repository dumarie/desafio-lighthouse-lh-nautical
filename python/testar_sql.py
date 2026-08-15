import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

def executar_questao_4():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔌 Conectado ao PostgreSQL. Executando a Questão 4.1...\n")

        # ----------------------------------------------------------------------
        # 1. Consulta para detalhar quem são os 10 Clientes Fiéis (Top 10)
        # ----------------------------------------------------------------------
        query_top10 = """
        WITH resumo_pedidos AS (
            SELECT 
                customer_id,
                COUNT(DISTINCT id) AS frequencia,
                SUM(total) AS faturamento_total,
                SUM(total) / COUNT(DISTINCT id) AS ticket_medio
            FROM orders
            GROUP BY customer_id
        ),
        diversidade_cliente AS (
            SELECT 
                o.customer_id,
                COUNT(DISTINCT p.category_id) AS diversidade_categorias
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN product_variants pv ON oi.product_variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            GROUP BY o.customer_id
        )
        SELECT 
            rp.customer_id,
            rp.frequencia,
            rp.faturamento_total,
            rp.ticket_medio,
            dc.diversidade_categorias
        FROM resumo_pedidos rp
        JOIN diversidade_cliente dc ON rp.customer_id = dc.customer_id
        WHERE dc.diversidade_categorias >= 13
        ORDER BY rp.ticket_medio DESC, rp.customer_id ASC
        LIMIT 10;
        """
        
        cursor.execute(query_top10)
        top10 = cursor.fetchall()
        
        print("="*75)
        print("🏆 TOP 10 CLIENTES DE ELITE (Diversidade >= 13 Categorias)")
        print("="*75)
        print(f"{'ID Cliente':<12} | {'Frequência':<10} | {'Faturamento Total':<20} | {'Ticket Médio':<20} | {'Categorias':<10}")
        print("-" * 75)
        for row in top10:
            print(f"{row[0]:<12} | {row[1]:<10} | R$ {row[2]:>16,.2f} | R$ {row[3]:>16,.2f} | {row[4]:<10}")
            
        # ----------------------------------------------------------------------
        # 2. Consulta Oficial da Questão 4.1 (Categoria com mais itens comprados)
        # ----------------------------------------------------------------------
        query_final = """
        WITH resumo_pedidos AS (
            SELECT 
                customer_id,
                COUNT(DISTINCT id) AS frequencia,
                SUM(total) AS faturamento_total,
                SUM(total) / COUNT(DISTINCT id) AS ticket_medio
            FROM orders
            GROUP BY customer_id
        ),
        diversidade_cliente AS (
            SELECT 
                o.customer_id,
                COUNT(DISTINCT p.category_id) AS diversidade_categorias
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN product_variants pv ON oi.product_variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            GROUP BY o.customer_id
        ),
        top10_clientes_elite AS (
            SELECT 
                rp.customer_id,
                rp.ticket_medio,
                dc.diversidade_categorias
            FROM resumo_pedidos rp
            JOIN diversidade_cliente dc ON rp.customer_id = dc.customer_id
            WHERE dc.diversidade_categorias >= 13
            ORDER BY rp.ticket_medio DESC, rp.customer_id ASC
            LIMIT 10
        )
        SELECT 
            c.id AS category_id,
            c.name AS nome_categoria,
            SUM(oi.quantity) AS quantidade_total_itens
        FROM top10_clientes_elite t10
        JOIN orders o ON t10.customer_id = o.customer_id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN product_variants pv ON oi.product_variant_id = pv.id
        JOIN products p ON pv.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        GROUP BY c.id, c.name
        ORDER BY quantidade_total_itens DESC
        LIMIT 1;
        """
        
        cursor.execute(query_final)
        resultado = cursor.fetchone()
        
        print("\n" + "="*75)
        print("📦 CATEGORIA MAIS VENDIDA PARA O TOP 10 CLIENTES DE ELITE")
        print("="*75)
        if resultado:
            print(f"• ID da Categoria:          {resultado[0]}")
            print(f"• Nome da Categoria:        {resultado[1]}")
            print(f"• Total de Itens Comprados: {resultado[2]:,.0f} unidades")
        print("="*75 + "\n")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Ocorreu um erro ao executar a consulta: {e}")

if __name__ == '__main__':
    executar_questao_4()