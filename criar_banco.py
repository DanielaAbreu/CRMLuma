import sqlite3

# Criação do banco de dados
conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Tabela de clientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    observacoes TEXT
)
''')

# Tabela de casos
cursor.execute('''
CREATE TABLE IF NOT EXISTS casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT DEFAULT 'Em aberto',
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
)
''')

conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")
