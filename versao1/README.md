# 🏋️ Sistema de Academia com Flask e PostgreSQL

Este projeto é um sistema simples de **gerenciamento de academia** feito em **Python (Flask)** e **PostgreSQL**, que permite inserir dados diretamente pelo **terminal**, sem necessidade de interface web.

Você pode cadastrar:
- Alunos
- Instrutores
- Planos
- Treinos
- Relacionar Treinos e Planos aos Alunos

---

## 📂 Estrutura do Projeto

/academia_app/
│
├── app.py # Código principal do sistema
├── config.py # Configurações do banco de dados
├── README.md # Documento de instruções
└── requirements.txt # Dependências do projeto

## Ative o venv

python -m venv venv

## Instalar blibliotecas

pip install -r requirements.txt

## Edite o arquivo config.py com suas credenciais do banco:

DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'academia',
    'user': 'postgres',
    'password': 'sua_senha_aqui',
    'port': 5432
}

## Execução do Sistema

python app.py
