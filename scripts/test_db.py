from db import create_table, insert_movie

create_table()
insert_movie("Teste Filme", "Descrição de teste", "Avengers")

print("Tabela criada e registro inserido com sucesso.")