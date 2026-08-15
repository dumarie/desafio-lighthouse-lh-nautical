-- ==============================================================================
-- QUESTÃO 5.1: DIMENSÃO DE DATAS E MÉDIA DE VENDAS POR DIA DA SEMANA (POS)
-- BANCO DE DADOS: PostgreSQL
-- ==============================================================================

WITH min_max_datas AS (
    -- 1. Identifica a menor e a maior data de venda
    SELECT 
        MIN(created_at::date) AS data_inicio,
        MAX(created_at::date) AS data_fim
    FROM orders
),

calendario AS (
    -- 2. Constroi a dimensão de datas completa e mapeia os dias da semana em português
    SELECT 
        d.data::date AS data,
        EXTRACT(DOW FROM d.data) AS dia_semana_num,
        CASE EXTRACT(DOW FROM d.data)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana_nome
    FROM min_max_datas m,
    LATERAL generate_series(m.data_inicio, m.data_fim, INTERVAL '1 day') AS d(data)
),

vendas_diarias_pos AS (
    -- 3. Agrupa o faturamento diário apenas para lojas físicas (channel/store_type = pos)
    SELECT 
        created_at::date AS data,
        SUM(total) AS total_vendas
    FROM orders
    WHERE LOWER(channel) = 'pos'
    GROUP BY created_at::date
),

vendas_calendario_completo AS (
    -- 4. LEFT JOIN entre calendário e vendas, convertendo NULL em 0 para dias sem venda
    SELECT 
        c.data,
        c.dia_semana_num,
        c.dia_semana_nome,
        COALESCE(v.total_vendas, 0) AS faturamento_diario
    FROM calendario c
    LEFT JOIN vendas_diarias_pos v ON c.data = v.data
)

-- 5. Calcula a média real de vendas considerando todos os dias do calendário
SELECT 
    vcc.dia_semana_nome AS dia_da_semana,
    COUNT(vcc.data) AS total_dias_no_periodo,
    SUM(vcc.faturamento_diario) AS faturamento_total,
    ROUND(AVG(vcc.faturamento_diario), 2) AS media_vendas_diarias
FROM vendas_calendario_completo vcc
GROUP BY vcc.dia_semana_num, vcc.dia_semana_nome
ORDER BY media_vendas_diarias ASC;
