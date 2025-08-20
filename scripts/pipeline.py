import requests
from datetime import date, timedelta, datetime
import mysql.connector




# Criando classe para iniciar a pipeline
class WeatherPipeline:
    """
    Uma classe para orquestrar um pipeline de extração e transformação dos dados
    de clima da API oficial OpenWeather
    """
    base_url_atual = 'https://api.openweathermap.org/data/2.5/weather'
    base_url_previsao = 'https://api.openweathermap.org/data/2.5/forecast'

    def __init__(self, api_key, city, db_config):
        self.api_key = api_key
        self.city = city
        self.db_config = db_config
        self.connection = self._get_db_connetion()
        self.current_data = None
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
            'lang':'pt_br'
        }
        try:
            response = requests.get(self.base_url_atual, params= params)
            response.raise_for_status()
            data = response.json()

            main_data = data.get('main',{})
            self.current_data = {
                'cidade': data.get('name'),
                'temperatura_atual': main_data.get('temp'),
                'sensacao_termica': main_data.get('feels_like'),
                'clima': data.get('weather', [{}])[0].get('description')
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
            'lang':'pt_br'
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
            self.processed_data = []
            return

        print('Trasformando dados da previsão futura...')
        hoje = date.today()
        limite_data = hoje + timedelta(days=4)
        previsoes_diarias = {}

        for previsao in self.raw_data:
            main_data = previsao.get('main', {})
            weather_data = previsao.get('weather', [{}])[0] 

            timestamp = datetime.strptime(previsao['dt_txt'],'%Y-%m-%d %H:%M:%S')
            data_previsao = timestamp.date()

            if hoje < data_previsao < limite_data:
                temp_atual = main_data.get('temp')
                if temp_atual is None: continue
                
                clima_atual = weather_data.get('description')

                if data_previsao not in previsoes_diarias:
                    previsoes_diarias[data_previsao] = {
                        'data': data_previsao.strftime('%Y-%m-%d'),
                        'temp_max':temp_atual,
                        'clima': clima_atual
                    }
                else:
                    if temp_atual > previsoes_diarias[data_previsao]['temp_max']:
                        previsoes_diarias[data_previsao]['temp_max'] = temp_atual
                        previsoes_diarias[data_previsao]['clima'] = clima_atual
        
        self.processed_data = list(previsoes_diarias.values())
        print(f'Transformação concluída ! {len(self.processed_data)} dias processados.')
    
    def run(self):
        """
        Executa todas as pipelines
        """
        self.extract_prev_atual()
        self.extract_prev()
        self.transform_prev()