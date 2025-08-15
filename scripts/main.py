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
