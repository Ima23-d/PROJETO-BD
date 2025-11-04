import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="meu_banco",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        print("Conexão estabelecida com sucesso!")
        return conexao
    except Exception as erro:
        print("Erro ao conectar ao banco de dados:", erro)
        return None


def criar_tabelas(con):
    ddl = """
    CREATE TABLE IF NOT EXISTS Alunos (
        ID_Aluno SERIAL PRIMARY KEY,
        Nome_Aluno VARCHAR(100) NOT NULL,
        CPF VARCHAR(14) UNIQUE NOT NULL,
        Data_Nascimento DATE NOT NULL,
        Idade INT NOT NULL,
        Peso DECIMAL(5,2) NOT NULL,
        Gordura_Corporal DECIMAL(5,2),
        Nivel VARCHAR(20),
        Deficiencia VARCHAR(100),
        Email VARCHAR(100) NOT NULL,
        Sexo VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Instrutores (
        ID_Instrutor SERIAL PRIMARY KEY,
        Nome VARCHAR(100) NOT NULL,
        CREF VARCHAR(20) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Planos (
        ID_Planos SERIAL PRIMARY KEY,
        Nome_Plano VARCHAR(100) NOT NULL,
        Descricao TEXT,
        Valor DECIMAL(10,2) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Treinos (
        ID_Treinos SERIAL PRIMARY KEY,
        Especificacoes TEXT NOT NULL,
        ID_Instrutor INT NOT NULL,
        FOREIGN KEY (ID_Instrutor) REFERENCES Instrutores(ID_Instrutor)
    );

    CREATE TABLE IF NOT EXISTS Treinos_Alunos (
        ID_Aluno INT NOT NULL,
        ID_Treinos INT NOT NULL,
        PRIMARY KEY (ID_Aluno, ID_Treinos),
        FOREIGN KEY (ID_Aluno) REFERENCES Alunos(ID_Aluno),
        FOREIGN KEY (ID_Treinos) REFERENCES Treinos(ID_Treinos)
    );

    CREATE TABLE IF NOT EXISTS Escolhe (
        ID_Aluno INT NOT NULL,
        ID_Planos INT NOT NULL,
        PRIMARY KEY (ID_Aluno, ID_Planos),
        FOREIGN KEY (ID_Aluno) REFERENCES Alunos(ID_Aluno),
        FOREIGN KEY (ID_Planos) REFERENCES Planos(ID_Planos)
    );
    """
    cursor = con.cursor()
    cursor.execute(ddl)
    con.commit()
    print("Tabelas criadas com sucesso (ou já existiam).")


# ---------- CRUD SIMPLES ----------
def cadastrar_instrutor(con):
    nome = input("Nome do instrutor: ")
    cref = input("CREF: ")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Instrutores (Nome, CREF) VALUES (%s, %s)", (nome, cref))
    con.commit()
    print("Instrutor cadastrado com sucesso!")


def listar_instrutores(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Instrutores ORDER BY Nome;")  # usando ORDER BY
    registros = cursor.fetchall()
    print("\n--- Instrutores ---")
    for linha in registros:
        print(f"ID: {linha[0]} | Nome: {linha[1]} | CREF: {linha[2]}")


# ---------- MENU USANDO MATCH CASE ----------
def menu(con):
    while True:
        print("""
        ====== MENU PRINCIPAL ======
        1. Cadastrar Instrutor
        2. Listar Instrutores
        0. Sair
        """)
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite apenas números!")
            continue

        match opcao:
            case 1:
                cadastrar_instrutor(con)
            case 2:
                listar_instrutores(con)
            case 0:
                print("Encerrando o sistema...")
                break
            case _:
                print("Opção inválida. Tente novamente.")


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        criar_tabelas(conexao)
        menu(conexao)
        conexao.close()
        print("Conexão encerrada.")
