import requests



api_correios = 'www.api.correios.com.br'


def buscar_cep(cep):
    try:
        busca = requests.get(headers='', data=cep, url=api_correios)
    except:
        requests.RequestException('Falha ao fazer request')

    return busca