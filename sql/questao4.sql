-- ==============================================================================
-- QUESTÃO 4.1: ANÁLISE DOS 10 CLIENTES FIÉIS (TOP 10 TICKET MÉDIO & DIVERSIDADE)
-- BANCO DE DADOS: PostgreSQL
-- ==============================================================================

WITH resumo_pedidos AS (
    -- 1. Calcula Faturamento Total, Frequência e Ticket Médio por cliente
    SELECT 
        customer_id,
        COUNT(DISTINCT id) AS frequencia,
        SUM(total) AS faturamento_total,
        SUM(total) / COUNT(DISTINCT id) AS ticket_medio
    FROM orders
    GROUP BY customer_id
),

diversidade_cliente AS (
    -- 2. Calcula a quantidade de categorias distintas compradas por cada cliente
    SELECT 
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
)

-- 3. Aplica o Filtro de Elite (>= 13 categorias) e retorna os Top 10 Clientes Fiéis
SELECT 
    rp.customer_id,
    rp.frequencia,
    rp.faturamento_total,
    rp.ticket_medio,
    dc.diversidade_categorias
FROM resumo_pedidos rp
JOIN diversidade_cliente dc ON rp.customer_id = dc.customer_id
WHERE dc.diversidade_categorias >= 13
ORDER BY 
    rp.ticket_medio DESC, 
    rp.customer_id ASC
LIMIT 10;