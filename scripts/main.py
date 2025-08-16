from pipeline import WeatherPipeline
from dotenv import load_dotenv
import os
import json

def salvar(dados, nome_pasta, nome_arquivo):
    """
    Salva os dados em um arquivo .json dentro da pasta dados_salvos
    """
    if not nome_arquivo.endwith('.json'):
        print(f'Aviso: O nome do arquivo "{nome_arquivo}" foi alterado para terminar com .json')
        nome_arquivo += '.json'

    os.makedirs(nome_pasta, exist_ok=True)

    caminho_completo = os.path.join(nome_pasta,nome_arquivo)
    try:
        with open(caminho_completo, 'w', encoding= 'utf-8') as f:
            json.dump(dados,f, indent=4, ensure_ascii= False)
        print('Dados salvos !')
    except IOError as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    # carregando a chave da api
    load_dotenv()

    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    if not API_KEY:
        raise ValueError('A chave da api "OPENWEATHER_API_KEY" não foi encontrada. Verifique o arquivo')

    city = 'Santos,BR' #input('Digite o nome da cidade que deseja buscar os dados, certivique que esetaja escrito corretamente e que a cidade exista !')

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
    
