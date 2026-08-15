import os
import csv
import psycopg2

# ==============================================================================
# CONFIGURAÇÕES DE CONEXÃO COM O POSTGRESQL
# (Ajuste os valores abaixo de acordo com as credenciais do seu banco de dados)
# ==============================================================================
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"       # Nome do seu banco de dados
DB_USER = "postgres"       # Seu usuário do PostgreSQL
DB_PASS = "postgres"      # Sua senha do PostgreSQL

DIRETORIO_CSVS = "."
ARQUIVO_SCHEMA = "schema.sql"


def carregar_dados_banco():
    """
    Conecta ao PostgreSQL, executa o schema.sql e carrega todos os CSVs
    sem realizar nenhuma limpeza ou tratamento nos dados.
    """
    try:
        print("🔌 Conectando ao banco de dados PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        print("✅ Conexão estabelecida com sucesso!\n")

        # ----------------------------------------------------------------------
        # 1. Executa o schema.sql para criar a estrutura das tabelas
        # ----------------------------------------------------------------------
        if os.path.exists(ARQUIVO_SCHEMA):
            print(f"📜 Criando tabelas a partir de '{ARQUIVO_SCHEMA}'...")
            with open(ARQUIVO_SCHEMA, 'r', encoding='utf-8') as f_schema:
                cursor.execute(f_schema.read())
            conn.commit()
            print("✅ Estrutura de tabelas criada no banco!\n")
        else:
            print(f"⚠️ Arquivo '{ARQUIVO_SCHEMA}' não encontrado na pasta local.\n")

        # ----------------------------------------------------------------------
        # 2. Carrega cada arquivo CSV bruto para a sua respetiva tabela
        # ----------------------------------------------------------------------
        arquivos_csv = [f for f in os.listdir(DIRETORIO_CSVS) if f.lower().endswith('.csv')]

        print("📥 Iniciando o carregamento dos CSVs...")
        for arq in sorted(arquivos_csv):
            nome_tabela = os.path.splitext(arq)[0].lower().strip()
            caminho_csv = os.path.join(DIRETORIO_CSVS, arq)

            with open(caminho_csv, 'r', encoding='utf-8-sig', errors='replace') as f_csv:
                # Instrução COPY nativa do Postgres: Carga ultra-rápida e sem filtros
                sql_copy = f"""
                    COPY {nome_tabela}
                    FROM STDIN
                    WITH (FORMAT csv, HEADER true, DELIMITER ',');
                """
                cursor.copy_expert(sql=sql_copy, file=f_csv)

            conn.commit()
            print(f"  • Tabela '{nome_tabela}' carregada com sucesso!")

        # ----------------------------------------------------------------------
        # 3. Validação - Questão 3.2 (Contagem de linhas acumuladas)
        # ----------------------------------------------------------------------
        tabelas_validacao = ['customers', 'orders', 'order_items', 'payments']
        total_acumulado = 0

        print("\n📊 --- RESPOSTA DA VALIDAÇÃO (Questão 3.2) ---")
        for tab in tabelas_validacao:
            cursor.execute(f"SELECT COUNT(*) FROM {tab};")
            qtd_linhas = cursor.fetchone()[0]
            total_acumulado += qtd_linhas
            print(f"  • {tab}: {qtd_linhas:,} linhas")

        print("--------------------------------------------------")
        print(f"🔥 TOTAL SOMADO DAS 4 TABELAS: {total_acumulado:,} linhas")
        print("--------------------------------------------------\n")

        cursor.close()
        conn.close()
        print("🎉 Processo de carga concluído com sucesso!")

    except Exception as e:
        print(f"\n❌ Ocorreu um erro no carregamento: {e}")


if __name__ == "__main__":
    carregar_dados_banco()