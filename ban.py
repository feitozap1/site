import sqlite3

print("SISTEMA DE BANIMENTO DO USUÁRIO")
print()

# CONEXÃO COM O BANCO
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

# PEGA OS USUÁRIOS CADASTRADOS
cursor.execute("SELECT id, nome, email FROM usuarios")
usuarios = cursor.fetchall()

# VERIFICA SE EXISTEM USUÁRIOS
if not usuarios:
    print("Nenhum usuário cadastrado.")

else:

    # MOSTRA OS USUÁRIOS
    print("USUÁRIOS CADASTRADOS")
    print()

    for pessoa in usuarios:
        print(f"ID: {pessoa[0]}")
        print(f"Nome: {pessoa[1]}")
        print(f"Email: {pessoa[2]}")
        print("--------------------")

    # PEDE O ID
    try:
        id_usuario = int(input("Digite o ID do usuário que deseja excluir: "))

    except ValueError:
        print("ID inválido.")

    else:

        # VERIFICA SE O ID EXISTE
        cursor.execute(
            "SELECT id FROM usuarios WHERE id = ?",
            (id_usuario,)
        )

        usuario = cursor.fetchone()

        if usuario:

            # EXCLUI O USUÁRIO
            cursor.execute(
                "DELETE FROM usuarios WHERE id = ?",
                (id_usuario,)
            )

            conexao.commit()

            print()
            print("Usuário excluído com sucesso!")

            # PEGA OS USUÁRIOS ATUALIZADOS
            cursor.execute("SELECT id, nome, email FROM usuarios")
            usuarios = cursor.fetchall()

            # ATUALIZA O usuarios.txt
            with open("usuarios.txt", "w", encoding="utf-8") as arquivo:

                for pessoa in usuarios:
                    arquivo.write(f"ID: {pessoa[0]}\n")
                    arquivo.write(f"Nome: {pessoa[1]}\n")
                    arquivo.write(f"Email: {pessoa[2]}\n")
                    arquivo.write("-------------------\n")

            print("Arquivo usuarios.txt atualizado!")

        else:
            print()
            print("Usuário não encontrado.")

# FECHA O BANCO
conexao.close()