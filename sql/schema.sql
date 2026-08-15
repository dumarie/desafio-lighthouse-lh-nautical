-- ==========================================================
-- SCHEMA AUTOMÁTICO GERADO PARA POSTGRESQL
-- Descrição: Instruções DDL para criação do Banco de Dados ERP
-- Gerado em: 2026-08-11 13:12:13
-- ==========================================================

-- ----------------------------------------------------------
-- 1. Instrução para criação da tabela 'addresses' (Endereços)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS addresses CASCADE;
CREATE TABLE addresses (
    id INTEGER,
    customer_id INTEGER,
    address_type VARCHAR(50),
    postal_code VARCHAR(50),
    street VARCHAR(70),
    number INTEGER,
    complement VARCHAR(50),
    district VARCHAR(66),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    is_primary VARCHAR(50)
);

-- ----------------------------------------------------------
-- 2. Instrução para criação da tabela 'attributes' (Atributos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS attributes CASCADE;
CREATE TABLE attributes (
    id INTEGER,
    name VARCHAR(50),
    data_type VARCHAR(50)
);

-- ----------------------------------------------------------
-- 3. Instrução para criação da tabela 'brands' (Marcas)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS brands CASCADE;
CREATE TABLE brands (
    id INTEGER,
    name VARCHAR(50),
    country VARCHAR(50),
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 4. Instrução para criação da tabela 'categories' (Categorias)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS categories CASCADE;
CREATE TABLE categories (
    id INTEGER,
    name VARCHAR(50),
    slug VARCHAR(50),
    parent_category_id INTEGER,
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 5. Instrução para criação da tabela 'customers' (Clientes)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers (
    id INTEGER,
    person_type VARCHAR(50),
    legal_name VARCHAR(62),
    trade_name VARCHAR(54),
    tax_id BIGINT,
    state_registration VARCHAR(50),
    email VARCHAR(94),
    phone VARCHAR(50),
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 6. Instrução para criação da tabela 'employees' (Funcionários)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS employees CASCADE;
CREATE TABLE employees (
    id INTEGER,
    full_name VARCHAR(50),
    cpf BIGINT,
    email VARCHAR(92),
    role VARCHAR(50),
    primary_location_id INTEGER,
    hire_date DATE,
    termination_date DATE,
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 7. Instrução para criação da tabela 'fiscal_invoices' (Notas Fiscais)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS fiscal_invoices CASCADE;
CREATE TABLE fiscal_invoices (
    id INTEGER,
    order_id INTEGER,
    nfe_number VARCHAR(50),
    nfe_access_key VARCHAR(50),
    series INTEGER,
    issued_at TIMESTAMP,
    status VARCHAR(50),
    total_amount NUMERIC(15, 2),
    xml_storage_uri VARCHAR(138),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 8. Instrução para criação da tabela 'goods_receipt_items' (Itens do Recebimento)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS goods_receipt_items CASCADE;
CREATE TABLE goods_receipt_items (
    id INTEGER,
    goods_receipt_id INTEGER,
    purchase_order_item_id INTEGER,
    quantity_received NUMERIC(15, 2)
);

-- ----------------------------------------------------------
-- 9. Instrução para criação da tabela 'goods_receipts' (Recebimentos de Mercadoria)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS goods_receipts CASCADE;
CREATE TABLE goods_receipts (
    id INTEGER,
    purchase_order_id INTEGER,
    received_by_employee_id INTEGER,
    received_at TIMESTAMP,
    notes VARCHAR(50),
    created_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 10. Instrução para criação da tabela 'locations' (Locais/Estoque/Lojas)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS locations CASCADE;
CREATE TABLE locations (
    id INTEGER,
    name VARCHAR(50),
    location_type VARCHAR(50),
    postal_code VARCHAR(50),
    street VARCHAR(50),
    number INTEGER,
    complement VARCHAR(50),
    district VARCHAR(54),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 11. Instrução para criação da tabela 'order_items' (Itens do Pedido)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS order_items CASCADE;
CREATE TABLE order_items (
    id INTEGER,
    order_id INTEGER,
    product_variant_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(15, 2),
    icms_rate NUMERIC(15, 2),
    ipi_rate NUMERIC(15, 2),
    line_total NUMERIC(15, 2)
);

-- ----------------------------------------------------------
-- 12. Instrução para criação da tabela 'orders' (Pedidos de Venda)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
    id INTEGER,
    order_number VARCHAR(50),
    channel VARCHAR(50),
    customer_id INTEGER,
    salesperson_id INTEGER,
    location_id INTEGER,
    status VARCHAR(50),
    subtotal NUMERIC(15, 2),
    discount_amount NUMERIC(15, 2),
    total NUMERIC(15, 2),
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 13. Instrução para criação da tabela 'payments' (Pagamentos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS payments CASCADE;
CREATE TABLE payments (
    id INTEGER,
    order_id INTEGER,
    method VARCHAR(50),
    installments INTEGER,
    amount NUMERIC(15, 2),
    status VARCHAR(50),
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 14. Instrução para criação da tabela 'product_suppliers' (Fornecedores de Produtos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS product_suppliers CASCADE;
CREATE TABLE product_suppliers (
    product_variant_id INTEGER,
    supplier_id INTEGER,
    supplier_sku VARCHAR(50),
    last_quoted_cost NUMERIC(15, 2),
    lead_time_days INTEGER,
    is_preferred VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 15. Instrução para criação da tabela 'product_variants' (Variantes de Produtos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS product_variants CASCADE;
CREATE TABLE product_variants (
    id INTEGER,
    product_id INTEGER,
    sku VARCHAR(50),
    barcode_ean BIGINT,
    sale_price NUMERIC(15, 2),
    cost_price NUMERIC(15, 2),
    weight_kg NUMERIC(15, 2),
    icms_rate NUMERIC(15, 2),
    ipi_rate NUMERIC(15, 2),
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 16. Instrução para criação da tabela 'products' (Produtos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE products (
    id INTEGER,
    name VARCHAR(50),
    description VARCHAR(96),
    brand_id INTEGER,
    category_id INTEGER,
    ncm_code INTEGER,
    unit_of_measure VARCHAR(50),
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 17. Instrução para criação da tabela 'purchase_order_items' (Itens da Ordem de Compra)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS purchase_order_items CASCADE;
CREATE TABLE purchase_order_items (
    id INTEGER,
    purchase_order_id INTEGER,
    product_variant_id INTEGER,
    quantity_ordered INTEGER,
    unit_cost NUMERIC(15, 2),
    line_total NUMERIC(15, 2)
);

-- ----------------------------------------------------------
-- 18. Instrução para criação da tabela 'purchase_orders' (Ordens de Compra)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS purchase_orders CASCADE;
CREATE TABLE purchase_orders (
    id INTEGER,
    po_number VARCHAR(50),
    supplier_id INTEGER,
    buyer_id INTEGER,
    destination_location_id INTEGER,
    status VARCHAR(50),
    currency VARCHAR(50),
    subtotal NUMERIC(15, 2),
    total NUMERIC(15, 2),
    placed_at TIMESTAMP,
    expected_delivery_at DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 19. Instrução para criação da tabela 'return_items' (Itens Devolvidos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS return_items CASCADE;
CREATE TABLE return_items (
    id INTEGER,
    return_id INTEGER,
    order_item_id INTEGER,
    quantity NUMERIC(15, 2),
    action VARCHAR(50),
    exchange_variant_id INTEGER,
    unit_refund_amount NUMERIC(15, 2)
);

-- ----------------------------------------------------------
-- 20. Instrução para criação da tabela 'returns' (Devoluções)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS returns CASCADE;
CREATE TABLE returns (
    id INTEGER,
    return_number VARCHAR(50),
    order_id INTEGER,
    customer_id INTEGER,
    received_at_location_id INTEGER,
    status VARCHAR(50),
    reason VARCHAR(66),
    total_refund_amount NUMERIC(15, 2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 21. Instrução para criação da tabela 'stock_levels' (Níveis de Estoque)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS stock_levels CASCADE;
CREATE TABLE stock_levels (
    product_variant_id INTEGER,
    location_id INTEGER,
    quantity_on_hand NUMERIC(15, 2),
    reorder_point VARCHAR(255),
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 22. Instrução para criação da tabela 'stock_movements' (Movimentações de Estoque)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS stock_movements CASCADE;
CREATE TABLE stock_movements (
    id INTEGER,
    product_variant_id INTEGER,
    location_id INTEGER,
    movement_type VARCHAR(50),
    quantity NUMERIC(15, 2),
    reference_table VARCHAR(255),
    reference_id VARCHAR(255),
    employee_id VARCHAR(255),
    notes VARCHAR(68),
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 23. Instrução para criação da tabela 'suppliers' (Fornecedores)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS suppliers CASCADE;
CREATE TABLE suppliers (
    id INTEGER,
    legal_name VARCHAR(60),
    trade_name VARCHAR(50),
    country VARCHAR(50),
    tax_id VARCHAR(50),
    tax_id_type VARCHAR(50),
    email VARCHAR(60),
    phone BIGINT,
    contact_name VARCHAR(54),
    is_active VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ----------------------------------------------------------
-- 24. Instrução para criação da tabela 'variant_attribute_values' (Valores de Atributos)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS variant_attribute_values CASCADE;
CREATE TABLE variant_attribute_values (
    product_variant_id INTEGER,
    attribute_id INTEGER,
    value VARCHAR(50)
);