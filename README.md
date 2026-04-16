📄 README.md

# Desafio Técnico - RPA Wellbe

## 📌 Objetivo

Implementar um fluxo completo de extração, transformação e carregamento de dados (ETL) a partir do portal RPA Challenge, com persistência em banco de dados e geração de arquivos finais.

---

## 🧠 Contexto

A Wellbe atua com análise de dados de saúde corporativa, auxiliando empresas na redução de custos através da mensuração de indicadores e eficiência de programas de saúde.

Dentro desse contexto, este desafio simula um cenário de automação de coleta de dados externos, estruturação e disponibilização para análise.

---

## ⚙️ Tecnologias utilizadas

- Python 3
- Selenium (automação web)
- MySQL (persistência de dados)
- Pandas (análise e validação)
- SQLAlchemy (integração com banco)
- Jupyter Notebook (apresentação e validação)
- Numpy (apoio à manipulação de dados)

---

## 🏗️ Arquitetura da solução

A solução foi estruturada seguindo o conceito de **ETL (Extract, Transform, Load)**:

### 🔹 Extract

- Automação com Selenium para navegação no portal
- Coleta de dados da aba Movie Search
- Captura de links da aba Invoice Extraction

### 🔹 Transform

- Tratamento de textos (remoção de truncamentos e normalização)
- Estruturação dos dados em formato consistente
- Filtragem dos invoices específicos (2 e 4)

### 🔹 Load

- Persistência dos dados no MySQL
- Download dos arquivos
- Geração de arquivo ZIP final

---

## 📂 Estrutura do projeto

desafio-wellbe-rpa/
├── downloads/ # Arquivos baixados (invoices)
├── output/ # ZIP final gerado
├── notebooks/
│ └── desafio_wellbe.ipynb # Notebook de execução e validação
├── scripts/
│ ├── browser.py
│ ├── db.py
│ ├── movie_search.py
│ ├── invoice_extraction.py
│ └── main.py
├── sql/
│ ├── schema.sql
│ ├── queries.sql
│ └── dump_movies.sql
├── requirements.txt
└── README.md

---

## 🚀 Como executar o projeto

### 1. Criar ambiente virtual

```bash
python -m venv .venv
2. Ativar ambiente

Windows:

.venv\Scripts\activate

Linux/Mac:

source .venv/bin/activate
3. Instalar dependências
pip install -r requirements.txt
4. Configurar banco de dados

Criar banco:

CREATE DATABASE wellbe_rpa;

Atualizar credenciais no arquivo:

scripts/db.py
5. Executar pipeline completo
python scripts/main.py
📊 Etapas implementadas
🔹 1. Movie Search
Acesso ao site https://rpachallenge.com/
Navegação para aba "Movie Search"
Busca pelo termo "Avengers"
Extração de:
Nome do filme
Descrição completa
Armazenamento no MySQL
🔹 2. Invoice Extraction
Acesso à aba "Invoice Extraction"
Leitura da tabela dinâmica
Identificação dos invoices:
Invoice 2
Invoice 4
Download dos arquivos
Geração de um único ZIP contendo ambos
🗄️ Banco de dados

Tabela utilizada:

movies

Campos:

id
movie_name
description
search_term
created_at

Arquivos incluídos:

schema.sql → criação da tabela
queries.sql → consultas básicas
dump_movies.sql → dados exportados
📓 Notebook

O notebook (notebooks/desafio_wellbe.ipynb) foi utilizado para:

Executar as etapas do pipeline
Validar os dados no banco
Exibir resultados com Pandas
Demonstrar o funcionamento da solução
📁 Outputs gerados
✔ Banco de dados populado

Filmes Avengers armazenados corretamente.

✔ Arquivos baixados
downloads/
├── invoice_2.jpg
└── invoice_4.jpg
✔ ZIP final
output/invoices_2_4.zip
⚠️ Observações técnicas
Foram utilizados WebDriverWait para garantir sincronização com a interface
Evitado uso de sleep() para maior performance e robustez
Extração feita via DOM completo para evitar dados truncados
Estrutura modular separando responsabilidades (browser, db, scripts)
💡 Considerações finais

A solução foi desenvolvida visando:

Clareza
Performance
Reprodutibilidade
Organização modular

Seguindo boas práticas de engenharia de dados e automação.

📬 Contato

Caso tenha qualquer dúvida sobre a implementação, fico à disposição para esclarecimentos.
```
