# Pipeline de Dados de Previsão do Tempo

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

## 📖 Sobre o Projeto

Este projeto implementa um pipeline de dados ETL (Extração, Transformação e Carga) completo, desenvolvido em Python. O objetivo é extrair dados de clima da API pública [OpenWeatherMap](https://openweathermap.org/api), processá-los e carregá-los em um **banco de dados MySQL** para persistência e análise futura.

O pipeline é capaz de buscar tanto as condições climáticas atuais quanto uma previsão consolidada para os próximos 3 dias para qualquer cidade do mundo.

## ✨ Funcionalidades

-   **Extração de Dados Atuais:** Coleta de dados como temperatura, sensação térmica e descrição do clima em tempo real.
-   **Extração de Previsão Futura:** Coleta de dados brutos de previsão para os próximos 5 dias, com intervalos de 3 horas.
-   **Transformação de Dados:** Processa os dados brutos da previsão para calcular a temperatura máxima de cada um dos próximos 3 dias, consolidando as informações.
-   **Carga de Dados:** Carrega os dados processados (atuais e futuros) em tabelas distintas no banco de dados MySQL.
-   **Configuração Segura:** Utiliza um arquivo `.env` para gerenciar a chave da API e as credenciais do banco de dados, evitando que informações sensíveis sejam expostas no código.

## 🏛️ Arquitetura do Pipeline

O fluxo de dados segue o padrão ETL clássico, com o carregamento sendo feito em um banco de dados relacional.

**API OpenWeatherMap** → **[E] Extração** (Python/Requests) → **[T] Transformação** (Python/Datetime) → **[L] Carga** (Banco de Dados MySQL)

## 🛠️ Tecnologias e Conceitos Utilizados

Este projeto foi construído utilizando as seguintes tecnologias e conceitos de engenharia de dados:

-   **Linguagem:** Python 3
-   **Banco de Dados:** MySQL
-   **Bibliotecas Principais:**
    -   `requests`: Para consumir a API REST.
    -   `python-dotenv`: Para gerenciamento seguro de credenciais.
    -   `mysql-connector-python`: Para conectar e manipular o banco de dados MySQL.
    -   `datetime`: Para lógica de datas e timestamps.
-   **Conceitos de Software:**
    -   **Programação Orientada a Objetos (OOP):** O pipeline é encapsulado na classe `WeatherPipeline`, organizando o código de forma coesa e reutilizável.
    -   **Modularidade:** O código é dividido em dois arquivos (`pipeline.py` e `main.py`), separando a lógica da ferramenta da sua execução.
-   **Desenvolvimento:**
    -   Um **Jupyter Notebook** foi utilizado para a prototipação, testes e validação inicial das funções antes da implementação final.

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
-   Python 3.8 ou superior
-   Um servidor MySQL 8.0 ou superior (local ou na nuvem)
-   Uma chave de API da [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).

### 2. Instalação
Clone o repositório e instale as dependências:
```bash
git clone [https://github.com/lucasghidini/Pipeline-previsao-tempo](https://github.com/lucasghidini/Pipeline-previsao-tempo)
cd Pipeline-previsao-tempo
```

Crie um arquivo `requirements.txt` com o conteúdo:
```
    requests
    python-dotenv
    mysql-connector-python
```
E instale com:
```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados
Conecte-se ao seu servidor MySQL e crie um banco de dados. Em seguida, crie as tabelas necessárias executando o script SQL abaixo:

<details>
<summary>Clique para ver o script SQL de criação das tabelas</summary>

```sql
CREATE TABLE clima_atual (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cidade VARCHAR(255),
    temperatura_atual DECIMAL(5, 2),
    sensacao_termica DECIMAL(5, 2),
    clima VARCHAR(255),
    data_extracao DATETIME
);

CREATE TABLE previsao_futura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cidade VARCHAR(255),
    data_previsao DATE,
    temp_max DECIMAL(5, 2),
    clima VARCHAR(255),
    data_extracao DATETIME
);
```
Os dados processados pelo pipeline são armazenados em duas tabelas no MySQL com os seguintes esquemas:

### Tabela: `clima_atual`
| Coluna              | Tipo de Dado      | Descrição                                         |
| ------------------- | ----------------- | ------------------------------------------------- |
| `id`                | INT (PK)          | Identificador único do registro.                  |
| `cidade`            | VARCHAR(255)      | Nome da cidade da qual os dados foram extraídos.  |
| `temperatura_atual` | DECIMAL(5, 2)     | Temperatura em graus Celsius no momento da coleta.|
| `sensacao_termica`  | DECIMAL(5, 2)     | Sensação térmica em graus Celsius.                |
| `clima`             | VARCHAR(255)      | Descrição textual do clima (ex: "céu limpo").     |
| `data_extracao`     | DATETIME          | Data e hora em que o pipeline executou a extração.|

### Tabela: `previsao_futura`
| Coluna          | Tipo de Dado      | Descrição                                           |
| --------------- | ----------------- | --------------------------------------------------- |
| `id`            | INT (PK)          | Identificador único do registro.                    |
| `cidade`        | VARCHAR(255)      | Nome da cidade da qual os dados foram extraídos.    |
| `data_previsao` | DATE              | A data futura para a qual a previsão se aplica.     |
| `temp_max`      | DECIMAL(5, 2)     | A temperatura máxima prevista para aquele dia.      |
| `clima`         | VARCHAR(255)      | A descrição do clima mais provável para aquele dia. |
| `data_extracao` | DATETIME          | Data e hora em que o pipeline executou a extração.  |

</details>

### 4. Configuração das Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto. Ele deve conter tanto a chave da API quanto as credenciais do seu banco de dados.

```
# Credenciais da API
OPENWEATHER_API_KEY=sua_chave_de_api_secreta_aqui

# Credenciais do Banco de Dados
DB_HOST=localhost
DB_USER=seu_usuario_do_banco
DB_PASSWORD=sua_senha_do_banco
DB_NAME=nome_do_seu_banco
```

### 5. Execução
Execute o arquivo `main.py`. O script solicitará que você digite o nome da cidade. Os dados serão inseridos diretamente nas tabelas do MySQL.

```bash
python main.py
```

Feito por Lucas Ghidini. 