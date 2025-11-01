from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

app = Flask(__name__)

# -------------------------------------------------
# FUNÇÃO DE CONEXÃO AO BANCO
# -------------------------------------------------
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


# -------------------------------------------------
# INSERÇÃO NAS TABELAS
# -------------------------------------------------
def inserir_aluno():
    print("\n=== Inserir Aluno ===")
    nome = input("Nome do aluno: ")
    cpf = input("CPF: ")
    data_nasc = input("Data de nascimento (AAAA-MM-DD): ")
    idade = int(input("Idade: "))
    peso = float(input("Peso (kg): "))
    gordura = input("Gordura corporal (%): ")
    gordura = float(gordura) if gordura else None
    nivel = input("Nível (básico, intermediário, avançado): ")
    deficiencia = input("Deficiência (ou deixe vazio): ")
    email = input("Email: ")
    sexo = input("Sexo: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Alunos (Nome_Aluno, CPF, Data_Nascimento, Idade, Peso, Gordura_Corporal, Nivel, Deficiencia, Email, Sexo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING ID_Aluno;
    """, (nome, cpf, data_nasc, idade, peso, gordura, nivel, deficiencia, email, sexo))
    aluno_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Aluno inserido com sucesso! ID: {aluno_id}\n")


def inserir_instrutor():
    print("\n=== Inserir Instrutor ===")
    nome = input("Nome: ")
    cref = input("CREF: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Instrutores (Nome, CREF)
        VALUES (%s, %s)
        RETURNING ID_Instrutor;
    """, (nome, cref))
    instrutor_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Instrutor inserido com sucesso! ID: {instrutor_id}\n")


def inserir_plano():
    print("\n=== Inserir Plano ===")
    nome = input("Nome do plano: ")
    descricao = input("Descrição: ")
    valor = float(input("Valor (R$): "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Planos (Nome_Plano, Descricao, Valor)
        VALUES (%s, %s, %s)
        RETURNING ID_Planos;
    """, (nome, descricao, valor))
    plano_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Plano inserido com sucesso! ID: {plano_id}\n")


def inserir_treino():
    print("\n=== Inserir Treino ===")
    especificacoes = input("Descrição do treino: ")
    id_instrutor = int(input("ID do instrutor responsável: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Treinos (Especificacoes, ID_Instrutor)
        VALUES (%s, %s)
        RETURNING ID_Treinos;
    """, (especificacoes, id_instrutor))
    treino_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Treino inserido com sucesso! ID: {treino_id}\n")


def vincular_treino_aluno():
    print("\n=== Vincular Treino a Aluno ===")
    id_aluno = int(input("ID do Aluno: "))
    id_treino = int(input("ID do Treino: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Treinos_alunos (ID_Aluno, ID_Treinos)
        VALUES (%s, %s);
    """, (id_aluno, id_treino))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Treino vinculado ao aluno com sucesso!\n")


def vincular_plano_aluno():
    print("\n=== Vincular Plano a Aluno ===")
    id_aluno = int(input("ID do Aluno: "))
    id_plano = int(input("ID do Plano: "))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Escolhe (ID_Aluno, ID_Planos)
        VALUES (%s, %s);
    """, (id_aluno, id_plano))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Plano vinculado ao aluno com sucesso!\n")


# -------------------------------------------------
# MENU DE OPÇÕES (INTERATIVO NO TERMINAL)
# -------------------------------------------------
def menu():
    while True:
        print("=========== MENU PRINCIPAL ===========")
        print("1 - Inserir Aluno")
        print("2 - Inserir Instrutor")
        print("3 - Inserir Plano")
        print("4 - Inserir Treino")
        print("5 - Vincular Treino a Aluno")
        print("6 - Vincular Plano a Aluno")
        print("0 - Sair")
        print("======================================")

        opcao = input("Escolha uma opção: ")

        match (opcao):
            case 1:
                inserir_aluno()
            case 2:
                inserir_instrutor()
            case 3:
                inserir_plano()
            case 4:
                inserir_treino()
            case 5:
                vincular_treino_aluno()
            case 6:
                vincular_plano_aluno()
            case 0:
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida")

# -------------------------------------------------
# EXECUÇÃO DO PROGRAMA
# -------------------------------------------------
if __name__ == "__main__":
    print("=== Sistema Academia conectado ao PostgreSQL ===\n")
    app.run(debug=True)
    menu()
