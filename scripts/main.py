import requests
import csv
from datetime import date, timedelta, datetime
from dotenv import load_dotenv
import os

# carregando a chave da api
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise ValueError('A chave da api "OPENWEATHER_API_KEY" não foi encontrada. Verifique o arquivo')



# Criando classe para iniciar a pipeline
class WeatherPipeline:
    """
    Uma classe para orquestrar um pipeline de extração e transformação dos dados
    de clima da API oficial OpenWeather
    """
    base_url_atual = 'https://api.openweathermap.org/data/2.5/weather'
    base_url_previsao = 'https://api.openweathermap.org/data/2.5/forecast'

    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city
        self.current_data = None
        self.raw_data = None
        self.processed_data = None
    
    def extract_prev_atual(self):
        """
        Método para a extrção dos dados da previsão atual da API,
        Guarda a lista bruta no atributo self.raw_data
        """
        print(f'Extraindo dados para {self.city}')
        params = {
            'q':self.city,
            'appid': self.api_key,
            'units': 'metric',
            'lang':'pt_bt'
        }
        try:
            response = requests.get(self.base_url_atual, params= params)
            response.raise_for_status()
            data = response.json()

            main_data = data.get('main',{})
            self.current_data = {
                'Cidade': data.get('name'),
                'Temperatura Atual': main_data.get('temp'),
                'Sensação Termica': main_data.get('feels_like'),
                'Clima': data.get('weather', [{}])[0].get('description')
            }
            print('Extração concluida !')
        except requests.exceptions.RequestException as e:
            print(f'Erro de extração: {e}')
            self.current_data = {}
    
    def extract_prev(self):
        """
        Metodo para extrair os dados da previsão futura da API
        """
        print(f'Extraidno a previsão futura para {self.city}')
        params = {
            'q':self.city,
            'appid': self.api_key,
            'units': 'metric',
            'lang':'pt_bt'
        }
        try:
            response = requests.get(self.base_url_previsao, params= params)
            response.raise_for_status()
            self.raw_data = response.json().get('list', [])
            print('Extração da previsão concluido !')
        except requests.exceptions.RequestException as e:
            print(f'Erro ao extrair: {e}')
            self.raw_data =[]