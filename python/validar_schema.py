import os
import re
import pandas as pd

def extrair_estruturas_sql(schema_path):
    """Lê o schema.sql e extrai as tabelas, colunas, tipos e limites de VARCHAR."""
    tabelas = {}
    tabela_atual = None
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        
    for linha in linhas:
        linha = linha.strip()
        
        # Detecta início de tabela
        match_create = re.search(r'CREATE TABLE\s+([a_zA-Z0-9_]+)', linha, re.IGNORECASE)
        if match_create:
            tabela_atual = match_create.group(1).lower()
            tabelas[tabela_atual] = {}
            continue
            
        # Detecta fim de tabela
        if tabela_atual and linha.startswith(')'):
            tabela_atual = None
            continue
            
        # Detecta definições de colunas
        if tabela_atual and linha and not linha.startswith('--') and not linha.startswith('DROP'):
            match_col = re.search(r'([a_zA-Z0-9_]+)\s+(VARCHAR\((\d+)\)|INTEGER|BIGINT|NUMERIC|TIMESTAMP|DATE)', linha, re.IGNORECASE)
            if match_col:
                nome_col = match_col.group(1).lower()
                tipo_dado = match_col.group(2).upper()
                tam_varchar = int(match_col.group(3)) if match_col.group(3) else None
                
                tabelas[tabela_atual][nome_col] = {
                    'tipo': tipo_dado,
                    'varchar_len': tam_varchar
                }
    return tabelas

def executar_validacao():
    schema_file = 'schema.sql'
    
    if not os.path.exists(schema_file):
        print("❌ Erro: O arquivo 'schema.sql' não foi encontrado na pasta!")
        return

    print("🔍 Lendo e analisando o 'schema.sql'...\n")
    schema_def = extrair_estruturas_sql(schema_file)
    
    erros = 0
    avisos = 0

    for nome_tabela, colunas in schema_def.items():
        csv_file = f"{nome_tabela}.csv"
        
        if not os.path.exists(csv_file):
            print(f"⚠️ CSV não encontrado para a tabela '{nome_tabela}': {csv_file}")
            continue
            
        df = pd.read_csv(csv_file)
        print(f"📊 Validando '{csv_file}' ({len(df)} registros)...")
        
        for nome_col, info_col in colunas.items():
            if nome_col not in df.columns:
                print(f"   ❌ [COLUNA AUSENTE] A coluna '{nome_col}' está no SQL, mas NÃO existe no CSV!")
                erros += 1
                continue
                
            # 1. Validação de tamanho para colunas VARCHAR
            if info_col['varchar_len']:
                limite_sql = info_col['varchar_len']
                # Pega o maior tamanho de texto do CSV nessa coluna
                maior_texto = df[nome_col].dropna().astype(str).str.len().max()
                maior_texto = int(maior_texto) if pd.notna(maior_texto) else 0
                
                if maior_texto > limite_sql:
                    print(f"   🚨 [ERRO DE TAMANHO] Coluna '{nome_col}': maior texto no CSV tem {maior_texto} caracteres, mas o SQL só permite VARCHAR({limite_sql})!")
                    erros += 1
                else:
                    print(f"   ✅ Coluna '{nome_col}' (VARCHAR {limite_sql}): Maior texto = {maior_texto} chars.")

            # 2. Validação para BIGINT/INTEGER com caracteres não numéricos
            if 'BIGINT' in info_col['tipo'] or 'INTEGER' in info_col['tipo']:
                amostra = df[nome_col].dropna().astype(str)
                contem_caracteres_especiais = amostra.str.contains(r'[^\d.]', regex=True).any()
                if contem_caracteres_especiais:
                    print(f"   ⚠️ [ALERTA DE TIPO] Coluna '{nome_col}' é {info_col['tipo']}, mas possui texto com formatação (ex: hífens, pontuação ou letras) no CSV!")
                    avisos += 1

    print("\n" + "="*60)
    print("RESULTADO FINAL DA VALIDAÇÃO:")
    if erros == 0 and avisos == 0:
        print("🎉 SUCESSO TOTAL! O 'schema.sql' é 100% compatível com os dados do projeto!")
    else:
        print(f"⚠️ Foram encontrados {erros} erro(s) crítico(s) e {avisos} alerta(s).")
    print("="*60)

if __name__ == '__main__':
    executar_validacao()