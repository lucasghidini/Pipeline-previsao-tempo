from pipeline import WeatherPipeline
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    # carregando a chave da api
    load_dotenv()

    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    if not API_KEY:
        raise ValueError('A chave da api "OPENWEATHER_API_KEY" não foi encontrada. Verifique o arquivo')

    city = 'São Paulo' #input('Digite o nome da cidade que deseja buscar os dados, certivique que esetaja escrito corretamente e que a cidade exista !')

    pipeline = WeatherPipeline(api_key=API_KEY, city= city)

    pipeline.run()

    print('RESULTADO DO FINAL DO PIPELINE')
    if pipeline.current_data:
        print('[Clima Atual]')
        print(f'Temperatura: {pipeline.current_data.get('temperatura_atual')}ºC')
        print(f'Sensação Termica: {pipeline.current_data.get('sensacao_termica')}ºc')
        print(f'Clima: {pipeline.current_data.get('clima')}')
    
    if pipeline.processed_data:
        print('[Previsão para os proximos dias]')
        for previsao in pipeline.processed_data:
            print(f'- {previsao['data']}: Temp. Max. {previsao['temp_max']}ºC, {previsao['clima']}')

    print('---Pipeline finalizado---')
    
