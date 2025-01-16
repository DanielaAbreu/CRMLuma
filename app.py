from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessário para mensagens de feedback

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('crm.db')
    conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários
    return conn

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página: Lista de clientes
@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

# Página para adicionar cliente
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        observacoes = request.form['observacoes']

        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nome, email, telefone, observacoes) VALUES (?, ?, ?, ?)',
                     (nome, email, telefone, observacoes))
        conn.commit()
        conn.close()
        flash('Cliente adicionado com sucesso!', 'success')
        return redirect(url_for('clientes'))
    return render_template('add.html')

# Página para buscar cliente
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    cliente_encontrado = None
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db_connection()
        cliente_encontrado = conn.execute(
            'SELECT * FROM clientes WHERE nome LIKE ?',
            ('%' + nome + '%',)
        ).fetchone()
        conn.close()
        if not cliente_encontrado:
            flash('Nenhum cliente encontrado com esse nome.', 'error')
    return render_template('buscar.html', cliente_encontrado=cliente_encontrado)

# Página para editar cliente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        observacoes = request.form['observacoes']
        conn.execute('UPDATE clientes SET nome = ?, email = ?, telefone = ?, observacoes = ? WHERE id = ?',
                     (nome, email, telefone, observacoes, id))
        conn.commit()
        conn.close()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes'))

    conn.close()
    return render_template('edit.html', cliente=cliente)

# Página para excluir cliente
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('clientes'))

# Página de configurações
@app.route('/configuracoes', methods=['GET', 'POST'])
def configuracoes():
    if request.method == 'POST':
        flash('Configurações salvas com sucesso!', 'success')
    return render_template('configuracoes.html')

# Página para gerenciar casos
@app.route('/casos', methods=['GET', 'POST'])
def casos():
    conn = get_db_connection()

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        descricao = request.form['descricao']
        conn.execute('INSERT INTO casos (cliente_id, descricao) VALUES (?, ?)', (cliente_id, descricao))
        conn.commit()
        flash('Caso criado com sucesso!', 'success')

    casos = conn.execute('''
        SELECT casos.id, clientes.nome, casos.descricao, casos.status
        FROM casos
        JOIN clientes ON casos.cliente_id = clientes.id
    ''').fetchall()
    clientes = conn.execute('SELECT id, nome FROM clientes').fetchall()
    conn.close()
    return render_template('casos.html', casos=casos, clientes=clientes)

# Página de relatórios
@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

if __name__ == '__main__':
    app.run(debug=True)
