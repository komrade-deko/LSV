import sqlite3

banco = sqlite3.connect('clientes.db')
cursor = banco.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS clientes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   email TEXT UNIQUE,
                   telefone INTEGER NOT NULL,
                   criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
        """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS produtos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   preco REAL NOT NULL,
                   estoque INTERGER DEFAULT 0
               )
        """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS pedidos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   cliente_id INTEGER NOT NULL,
                   data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   data_entrega TEXT NOT NULL,
                   numero_pedido INTEGER NOT NULL UNIQUE,
                   valor REAL NOT NULL,
                   FOREIGN KEY(cliente_id) REFERENCES clientes(id)
                   )
        """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS itens_pedido(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   produto_id INTEGER NOT NULL,
                   pedido_id INTEGER NOT NULL,
                   quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
                   FOREIGN KEY(produto_id) REFERENCES produtos(id),
                   FOREIGN KEY(pedido_id) REFERENCES pedidos(id)
                   )
        """)

banco.commit()
banco.close()