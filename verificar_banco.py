import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Exibir as tabelas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas no banco de dados:")
for tabela in tabelas:
    print(f"- {tabela[0]}")

conn.close()
