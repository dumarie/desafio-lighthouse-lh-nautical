import os
import csv
from datetime import datetime

# ----------------------------------------------------------------------
# Configurações
# ----------------------------------------------------------------------
DIRETORIO_CSVS = "."       # Pasta onde estão os CSVs ('.' significa a pasta atual)
ARQUIVO_SAIDA = "schema.sql"  # Nome do arquivo SQL de saída
AMOSTRA_LINHAS = 1000      # Quantidade de linhas para analisar e inferir o tipo


def inferir_tipo_coluna_postgres(valores):
    """
    Analisa uma lista de valores de uma coluna e retorna o tipo de dado
    mais adequado para o PostgreSQL.
    """
    # Remove valores em branco / nulos da amostragem
    valores_validos = [v.strip() for v in valores if v is not None and v.strip() != '']
    
    if not valores_validos:
        return "VARCHAR(255)"
    
    eh_inteiro = True
    eh_decimal = True
    eh_data = True
    eh_timestamp = True
    tamanho_maximo = 0
    
    for v in valores_validos:
        tamanho_maximo = max(tamanho_maximo, len(v))
        
        # Teste 1: Inteiro
        if eh_inteiro:
            try:
                int(v)
            except ValueError:
                eh_inteiro = False
                
        # Teste 2: Decimal
        if eh_decimal:
            try:
                float(v)
            except ValueError:
                eh_decimal = False
                
        # Teste 3: Data (YYYY-MM-DD)
        if eh_data:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                eh_data = False
                
        # Teste 4: Timestamp (YYYY-MM-DD HH:MM:SS)
        if eh_timestamp:
            try:
                # Trata possíveis frações de segundos ou formatos ISO
                v_clean = v.split('.')[0].replace('T', ' ')
                datetime.strptime(v_clean, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                eh_timestamp = False

    # Hierarquia de decisão para o PostgreSQL
    if eh_inteiro:
        return "BIGINT" if tamanho_maximo > 9 else "INTEGER"
    if eh_decimal:
        return "NUMERIC(15, 2)"
    if eh_timestamp:
        return "TIMESTAMP"
    if eh_data:
        return "DATE"
    
    # Se for texto
    if tamanho_maximo > 255:
        return "TEXT"
    else:
        # Garante uma margem confortável para o VARCHAR
        tamanho_coluna = max(tamanho_maximo * 2, 50)
        return f"VARCHAR({min(tamanho_coluna, 255)})"


def gerar_schema_sql(diretorio_origem, arquivo_destino):
    """
    Varre o diretório em busca de CSVs, infere os schemas e salva o SQL.
    """
    arquivos_csv = [f for f in os.listdir(diretorio_origem) if f.lower().endswith('.csv')]
    
    if not arquivos_csv:
        print(f"❌ Nenhum arquivo CSV encontrado em '{diretorio_origem}'.")
        return

    instrucoes_sql = []
    instrucoes_sql.append("-- ==========================================================")
    instrucoes_sql.append("-- SCHEMA AUTOMÁTICO GERADO PARA POSTGRESQL")
    instrucoes_sql.append(f"-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    instrucoes_sql.append("-- ==========================================================\n")

    for arq in sorted(arquivos_csv):
        nome_tabela = os.path.splitext(arq)[0].lower().strip()
        caminho_completo = os.path.join(diretorio_origem, arq)
        
        print(f"🔍 Analisando arquivo: {arq} -> Tabela: {nome_tabela}")
        
        try:
            # utf-8-sig evita caracteres ocultos do Excel no cabeçalho
            with open(caminho_completo, mode='r', encoding='utf-8-sig', errors='replace') as f:
                leitor = csv.reader(f)
                headers = next(leitor, None)
                
                if not headers:
                    print(f"⚠️ Arquivo {arq} está vazio. Pulando...")
                    continue
                
                # Coleta amostra de dados por coluna
                colunas_amostras = {h.strip(): [] for h in headers}
                
                for i, linha in enumerate(leitor):
                    if i >= AMOSTRA_LINHAS:
                        break
                    for h, val in zip(headers, linha):
                        colunas_amostras[h.strip()].append(val)
                
                # Monta a instrução CREATE TABLE
                sql_tabela = [f"DROP TABLE IF EXISTS {nome_tabela} CASCADE;"]
                sql_tabela.append(f"CREATE TABLE {nome_tabela} (")
                
                definioes_colunas = []
                for nome_coluna, amostra in colunas_amostras.items():
                    tipo_pg = inferir_tipo_coluna_postgres(amostra)
                    definioes_colunas.append(f"    {nome_coluna} {tipo_pg}")
                
                sql_tabela.append(",\n".join(definioes_colunas))
                sql_tabela.append(");\n")
                
                instrucoes_sql.append("\n".join(sql_tabela))
                
        except Exception as e:
            print(f"❌ Erro ao processar o arquivo {arq}: {e}")

    # Salva o arquivo schema.sql
    with open(arquivo_destino, mode='w', encoding='utf-8') as f_out:
        f_out.write("\n\n".join(instrucoes_sql))
        
    print(f"\n✅ Sucesso! O arquivo '{arquivo_destino}' foi gerado com sucesso.")


if __name__ == "__main__":
    gerar_schema_sql(DIRETORIO_CSVS, ARQUIVO_SAIDA)