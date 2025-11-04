import psycopg2

# Função para conectar ao banco de dados PostgreSQL
def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="meu_banco",   # Substitua pelo nome do seu banco
            user="postgres",      # Usuário do PostgreSQL
            password="1234",      # Senha do PostgreSQL
            host="localhost",     # Servidor
            port="5432"           # Porta padrão
        )
        print("✅ Conexão estabelecida com sucesso!")
        return conexao
    except Exception as erro:
        print("❌ Erro ao conectar ao banco de dados:", erro)
        return None


# Função para criar as tabelas com base no DDL fornecido
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

    try:
        cursor = con.cursor()
        cursor.execute(ddl)
        con.commit()
        print("📘 Todas as tabelas foram criadas (ou já existiam).")
    except Exception as erro:
        print("❌ Erro ao criar tabelas:", erro)


# Exemplo de inserção de dados
def inserir_instrutor(con, nome, cref):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO Instrutores (Nome, CREF) VALUES (%s, %s)",
            (nome, cref)
        )
        con.commit()
        print("✅ Instrutor inserido com sucesso!")
    except Exception as erro:
        print("❌ Erro ao inserir instrutor:", erro)


def listar_instrutores(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Instrutores")
        registros = cursor.fetchall()
        print("📋 Lista de instrutores:")
        for linha in registros:
            print(f"ID: {linha[0]} | Nome: {linha[1]} | CREF: {linha[2]}")
    except Exception as erro:
        print("❌ Erro ao listar instrutores:", erro)


# Programa principal
if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        criar_tabelas(conexao)

        # Inserção de exemplo
        inserir_instrutor(conexao, "Carlos Souza", "CREF12345")
        inserir_instrutor(conexao, "Marina Lopes", "CREF98765")

        listar_instrutores(conexao)

        conexao.close()
        print("🔒 Conexão encerrada.")
