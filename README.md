# Pipeline de Dados de Previsão do Tempo

## 📖 Sobre o Projeto

Este projeto implementa um pipeline de dados ETL (Extração, Transformação e Carga) completo, desenvolvido em Python. O objetivo é extrair dados de clima da API pública [OpenWeatherMap](https://openweathermap.org/api), processá-los e salvá-los em um formato estruturado.

O pipeline é capaz de buscar tanto as condições climáticas atuais quanto uma previsão consolidada para os próximos 3 dias para qualquer cidade do mundo. O resultado final é salvo localmente em arquivos `.json`.

## ✨ Funcionalidades

  - **Extração de Dados Atuais:** Coleta de dados como temperatura, sensação térmica e descrição do clima em tempo real.
  - **Extração de Previsão Futura:** Coleta de dados brutos de previsão para os próximos 5 dias, com intervalos de 3 horas.
  - **Transformação de Dados:** Processa os dados brutos da previsão para calcular a temperatura máxima de cada um dos próximos 3 dias, consolidando as informações em um formato simples e útil.
  - **Carga de Dados:** Salva os dados processados (atuais e futuros) em arquivos `.json` distintos em um diretório local.
  - **Configuração Segura:** Utiliza um arquivo `.env` para gerenciar a chave da API, evitando que informações sensíveis sejam expostas no código.

## 🏛️ Arquitetura do Pipeline

O fluxo de dados segue o padrão ETL clássico:

**API OpenWeatherMap** → **[E] Extração** (Python/Requests) → **[T] Transformação** (Python/Datetime) → **[L] Carga** (Arquivos JSON)

## 🛠️ Tecnologias e Conceitos Utilizados

Este projeto foi construído utilizando as seguintes tecnologias e conceitos de engenharia de dados:

  - **Linguagem:** Python 3
  - **Bibliotecas Principais:**
      - `requests`: Para realizar chamadas HTTP e consumir a API REST da OpenWeatherMap.
      - `python-dotenv`: Para o gerenciamento seguro de variáveis de ambiente (API Key).
      - `datetime`: Para manipulação e cálculos envolvendo datas e horas na etapa de transformação.
      - `os` e `json`: Para manipulação de arquivos e pastas, e para serialização dos dados no formato JSON.
  - **Conceitos de Software:**
      - **Programação Orientada a Objetos (OOP):** O pipeline é encapsulado na classe `WeatherPipeline`, organizando o código de forma coesa e reutilizável.
      - **Modularidade:** O código é dividido em dois arquivos (`pipeline.py` e `main.py`), separando a lógica da ferramenta (a classe) da sua execução.
  - **Desenvolvimento:**
      - Um **Jupyter Notebook** foi utilizado para a prototipação, testes e validação inicial das funções e da lógica de transformação antes da implementação final no script.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o pipeline em sua máquina local.

### 1\. Pré-requisitos

  - Python 3.8 ou superior
  - pip (gerenciador de pacotes do Python)
  - Uma chave de API da [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) (o plano gratuito é suficiente).

### 2\. Instalação

Primeiro, clone o repositório para a sua máquina:

```bash
git clone https://github.com/lucasghidini/Pipeline-de-Dados.git
```

Crie um arquivo chamado `requirements.txt` com o seguinte conteúdo:

```
requests
python-dotenv
```

Agora, instale as dependências:

```bash
pip install -r requirements.txt
```

### 3\. Configuração da API Key

Crie um arquivo chamado `.env` na raiz do projeto. Dentro dele, adicione sua chave da API da OpenWeatherMap da seguinte forma:

```
OPENWEATHER_API_KEY=sua_chave_de_api_secreta_aqui
```

### 4\. Execução

Para rodar o pipeline, execute o arquivo `main.py` a partir do seu terminal. O script solicitará que você digite o nome da cidade.

```bash
python main.py
```

Após a execução, os arquivos `clima_atual.json` e `previsao_futura.json` serão criados na pasta `dados_salvos`.

## 📂 Estrutura do Projeto

```
.
├── dados_salvos/           # Pasta onde os arquivos JSON de saída são salvos
├── .env                    # Arquivo de configuração da API Key (não versionado)
├── main.py                 # Ponto de entrada do programa, orquestra o pipeline
├── pipeline.py             # Módulo que contém a classe WeatherPipeline (a ferramenta)
├── requirements.txt        # Lista de dependências do projeto
└── README.md               # Este arquivo
```

## 📄 Exemplo de Saída

**`clima_atual.json`**

```json
{
    "cidade": "Santos",
    "temperatura_atual": 25.0,
    "sensacao_termica": 25.0,
    "clima": "céu limpo"
}
```

**`previsao_futura.json`**

```json
[
    {
        "data": "2025-08-16",
        "temp_max": 26.5,
        "clima": "nuvens dispersas"
    },
    {
        "data": "2025-08-17",
        "temp_max": 27.0,
        "clima": "chuva leve"
    },
    {
        "data": "2025-08-18",
        "temp_max": 25.8,
        "clima": "céu limpo"
    }
]
```