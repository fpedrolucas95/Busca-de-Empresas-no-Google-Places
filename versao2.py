import requests
import json
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning
from tenacity import retry, stop_after_attempt, wait_fixed

# Desativa avisos de solicitação insegura
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Parâmetros de pesquisa
termo_busca = "" # Insira dentro das aspas o termo que deseja pesquisar, tais como Escolas Técnicas, Faculdades, Cursos, entre outros. Você pode combinar mais de um termo de pesquisa utilizando o sinal de adição (+), por exemplo: "Faculdade+Curso Técnico."
localizacao = "" # Insira dentro das aspas a localização desejada para a busca
cursos_saude = [""] # Insira o curso que deseja buscar
num_resultados = 1 # Altere esse valor para a quantidade de resultados desejados
chave_api = "SUA_CHAVE_AQUI" # Coloque aqui sua chave de API do Google, você pode gerar uma em https://console.cloud.google.com/

# Função para verificar se algum curso na área de saúde está presente no site
@retry(stop=stop_after_attempt(25), wait=wait_fixed(5))
def cursos_relacionados_saude(url, cursos):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    try:
        pagina = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.ConnectionError:
        print(f"Conexão abortada, pulando o site: {url}")
        return False

    for curso in cursos:
        if curso.lower() in pagina.text.lower():
            return True
    return False

# Função para buscar locais
def busca_locais(chave_api, termo_busca, localizacao, num_resultados, cursos_saude):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={termo_busca}+{localizacao}&key={chave_api}"
    resposta = requests.get(url)
    resultados = json.loads(resposta.text)["results"]
    token_proxima_pagina = json.loads(resposta.text).get("next_page_token")

    instituicoes = []

    while True:
        for r in resultados:
            id_local = r["place_id"]
            detalhes_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id_local}&fields=name,formatted_address,formatted_phone_number,website&key={chave_api}"
            resposta = requests.get(detalhes_url)
            resultado_detalhes = json.loads(resposta.text)["result"]

            site = resultado_detalhes.get("website", "N/A")

            if site != "N/A" and cursos_relacionados_saude(site, cursos_saude):
                instituicao = {
                    "nome": resultado_detalhes["name"],
                    "endereco": resultado_detalhes["formatted_address"],
                    "telefone": resultado_detalhes.get("formatted_phone_number", "N/A"),
                    "email": site
                }

                if instituicao not in instituicoes:
                    instituicoes.append(instituicao)

            if len(instituicoes) >= num_resultados:
                return instituicoes

        if not token_proxima_pagina:
            break

        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={termo_busca}+{localizacao}&key={chave_api}&pagetoken={token_proxima_pagina}"
        resposta = requests.get(url)
        resultados = json.loads(resposta.text)["results"]
        token_proxima_pagina = json.loads(resposta.text).get("next_page_token")

    return instituicoes

# Busca locais e cria um Pandas DataFrame
instituicoes = busca_locais(chave_api, termo_busca, localizacao, num_resultados, cursos_saude)
df = pd.DataFrame(instituicoes)

# Exporta para um arquivo csv
df.to_csv("resultados.csv", index=False)
