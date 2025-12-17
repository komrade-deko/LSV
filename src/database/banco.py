import sqlite3

banco = sqlite3.connect('clientes.db')
cursor = banco.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS clientes(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nome TEXT NOT NULL,
#         email TEXT UNIQUE,
#         telefone INTEGER NOT NULL,
#         criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# """)
#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS produtos(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nome TEXT NOT NULL,
#         preco REAL NOT NULL,
#         estoque INTEGER DEFAULT 0
#     )
# """)
#
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_entrega TEXT NOT NULL,
        numero_pedido INTEGER UNIQUE,
        valor REAL NOT NULL,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
""")
#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS itens_pedido(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         produto_id INTEGER NOT NULL,
#         pedido_id INTEGER NOT NULL,
#         quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
#         FOREIGN KEY(produto_id) REFERENCES produtos(id),
#         FOREIGN KEY(pedido_id) REFERENCES pedidos(id)
#     )
# """)
#
# banco.commit()
#
# cursor.execute("SELECT COALESCE(MAX(numero_pedido), 22) + 1 FROM pedidos")
# proximo_numero = cursor.fetchone()[0]
#
# cursor.execute(
#     "UPDATE itens_pedido SET pedido_id = ? WHERE id = ?",
#     (22, 2)
# )
cursor.execute(
		"INSERT INTO itens_pedido (produto_id, pedido_id, quantidade) VALUES (?,?,?)",
		(20,23,40)
	)
# cursor.execute(
#     """
#     ALTER TABLE pedidos
#     ADD COLUMN status TEXT DEFAULT 'Em Produção'
#     """
# )
#
# cursor.execute("""
#     CREATE VIEW vw_itens_pedido_detalhados AS
# SELECT
#     ip.id,
#     ip.pedido_id,
#     ip.produto_id,
#     ip.quantidade,
#     p.nome as produto_nome,
#     p.preco as preco_unitario,
#     (ip.quantidade * p.preco) as total_item
# FROM itens_pedido ip
# INNER JOIN produtos p ON ip.produto_id = p.id;
# """)

# cursor.execute(
#     "DELETE FROM itens_pedido WHERE id = ?",
#     (1,)
# )

banco.commit()
banco.close()