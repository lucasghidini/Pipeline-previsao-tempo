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

    def transform_prev(self):
        """
        Método para transformar os dados brutos da previsão
        """
        if not self.raw_data:
            print('Transformação pulada: Não a dados de previsão para procesar')
            self.raw_data = []
            return

        print('Trasformando dados da previsão futura...')
        hoje = date.today()
        limite_data = hoje + timedelta(days=4)
        previsoes_diarias = {}

        for previsao in self.raw_data:
            timestamp = datetime.strptime(previsao['dt_txt'],'%Y-%m-%d %H:%M:%S')
            data_previsao = timestamp.date()

            if hoje < data_previsao < limite_data:
                temp_atual = previsao['main']['temp']

                if data_previsao not in previsoes_diarias:
                    previsoes_diarias[data_previsao] = {
                        'data': data_previsao.strftime('%Y-%m-%d'),
                        'temp_max':temp_atual,
                        'clima_representativo': previsao['weather'][0]['description']
                    }
                else:
                    if temp_atual > previsoes_diarias[data_previsao]['temp_max']:
                        previsoes_diarias[data_previsao]['temp_max'] = temp_atual
                        previsoes_diarias[data_previsao]['clima_representativo'] = previsao['weather'][0]['description']
        
        self.processed_data = list(previsoes_diarias.values())
        print(f'Transformação concluída ! {len(self.processed_data)} dias processados.')