
import sqlite3
import os

# --------------------------------------------------
# LOCAL DOS ARQUIVOS
# --------------------------------------------------

pasta_programa = os.path.dirname(os.path.abspath(__file__))

caminho_banco = os.path.join(pasta_programa, "banco.db")
caminho_txt = os.path.join(pasta_programa, "usuarios.txt")


# TESTE
print("================================")
print("PASTA DO PROGRAMA:")
print(pasta_programa)

print()
print("BANCO:")
print(caminho_banco)

print()
print("ARQUIVO TXT:")
print(caminho_txt)

print("================================")



# --------------------------------------------------
# CONEXÃO COM O BANCO
# --------------------------------------------------

conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()


# --------------------------------------------------
# CRIAÇÃO DA TABELA
# --------------------------------------------------

comandos_sql = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
"""

cursor.execute(comandos_sql)
conexao.commit()


# --------------------------------------------------
# FUNÇÃO PARA ATUALIZAR usuarios.txt
# --------------------------------------------------

def atualizar_arquivo():

    cursor.execute("SELECT id, nome, email, senha FROM usuarios")
    usuarios = cursor.fetchall()

    with open(caminho_txt, "w", encoding="utf-8") as arquivo:

        for pessoa in usuarios:

            arquivo.write(f"ID: {pessoa[0]}\n")
            arquivo.write(f"Nome: {pessoa[1]}\n")
            arquivo.write(f"Email: {pessoa[2]}\n")
            arquivo.write(f"Senha: {pessoa[3]}\n")
            arquivo.write("-------------------\n")

    print()
    print("usuarios.txt atualizado com sucesso!")
    print(f"Local: {caminho_txt}")
    print(f"Usuários salvos: {len(usuarios)}")


# --------------------------------------------------
# MENU
# --------------------------------------------------

while True:

    print()
    print("1 - Fazer login")
    print("2 - Cadastrar usuario")
    print("3 - Encerrar programa")
    print("4 - Listar usuarios")
    print("5 - Reiniciar sistema (Apagar todos os usuários)")
    print()

    try:

        opc = int(input("Digite a opção desejada: "))

    except ValueError:

        print("Opção inválida. Digite um número.")
        continue

    print()


    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    if opc == 1:

        usuario = input("Digite o nome do usuario: ")
        email = input("Digite o email do usuario: ")
        senha = input("Digite a senha do usuario: ")

        print()

        cursor.execute("""
        SELECT * FROM usuarios
        WHERE nome = ? AND email = ?
        """, (usuario, email))

        resultado = cursor.fetchone()

        if resultado:

            if resultado[3] == senha:

                print("Login realizado com sucesso!")
                print(f"Seja bem-vindo de volta, {usuario}!")

            else:

                print("Senha incorreta. Tente novamente.")

                trocar = input("Deseja trocar a senha? (s/n): ")

                if trocar.lower() == "s":

                    nova_senha = input("Digite a nova senha: ")

                    cursor.execute("""
                    UPDATE usuarios
                    SET senha = ?
                    WHERE nome = ? AND email = ?
                    """, (nova_senha, usuario, email))

                    conexao.commit()

                    print("Senha alterada com sucesso!")

        else:

            print("Usuario ou email não encontrados.")


    # --------------------------------------------------
    # CADASTRO
    # --------------------------------------------------

    elif opc == 2:

        usuario = input("Digite um nome de usuario: ")
        email = input("Digite um email: ")

        # VERIFICA USUARIO

        cursor.execute("""
        SELECT * FROM usuarios
        WHERE nome = ?
        """, (usuario,))

        usuario_existente = cursor.fetchone()


        # VERIFICA EMAIL

        cursor.execute("""
        SELECT * FROM usuarios
        WHERE email = ?
        """, (email,))

        email_existente = cursor.fetchone()


        if usuario_existente:

            print("Usuario já cadastrado.")

        elif email_existente:

            print("Email já cadastrado.")

        elif not email.endswith("@gmail.com"):

            print("Email inválido. Use um email do Gmail. (Exemplo: usuario@gmail.com)")

        else:

            senha = input("Digite uma senha: ")

            cursor.execute("""
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
            """, (usuario, email, senha))

            conexao.commit()

            print()
            print(f"O usuario {usuario} foi cadastrado com sucesso!")
            print(f"Email: {email}")

            # ATUALIZA O TXT

            atualizar_arquivo()


    # --------------------------------------------------
    # ENCERRAR
    # --------------------------------------------------

    elif opc == 3:

        print("Programa encerrado.")
        break


    # --------------------------------------------------
    # LISTAR USUARIOS
    # --------------------------------------------------

    elif opc == 4:

        cursor.execute("SELECT * FROM usuarios")

        usuarios = cursor.fetchall()

        print()

        if not usuarios:

            print("Nenhum usuario cadastrado.")

        else:

            for usuario in usuarios:

                id_usuario = usuario[0]
                nome = usuario[1]
                email = usuario[2]
                senha = usuario[3]

                print(f"ID: {id_usuario}")
                print(f"Nome: {nome}")
                print(f"Email: {email}")
                print(f"Senha: {senha}")
                print("--------------------")

     # --------------------------------------------------
    # REINICIA E EXCLUI OS USUARIOS
    # --------------------------------------------------
    
    elif opc == 5:

            cursor.execute("DELETE FROM usuarios")

            # Reinicia o contador do AUTOINCREMENT
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'usuarios'")

            conexao.commit()

            atualizar_arquivo()

            print("Todos os usuários foram removidos.")
            print("Sistema reiniciado. O próximo usuário terá ID 1.")


    else:

        print("Opção inválida.")


# --------------------------------------------------
# FECHA O BANCO
# --------------------------------------------------

conexao.close()
