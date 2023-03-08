import requests
import json
import pandas as pd

# Define os parâmetros de pesquisa
search_term = input("Digite o nicho de interesse: ")
location = input("Digite a localização de interesse: ")
# altere para a quantidade desejada de resultados
num_results = 20

# Defina a sua chave de API do Google Places
api_key = "sua_chave_aqui"

# Use a API para buscar locais
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_term}+{location}&key={api_key}"
response = requests.get(url)
results = json.loads(response.text)["results"]
next_page_token = json.loads(response.text).get("next_page_token")

# Busca telefone e e-mail de cada local
name = []
address = []
phone = []
email = []
for r in results[:num_results]:
    name.append(r["name"])
    address.append(r["formatted_address"])
    try:
        place_id = r["place_id"]
        # Solicitação para buscar telefone e e-mail
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website&key={api_key}"
        response = requests.get(url)
        result = json.loads(response.text)["result"]
        phone.append(result.get("formatted_phone_number", "N/A"))
        email.append(result.get("website", "N/A"))
    except:
        phone.append("N/A")
        email.append("N/A")

# Verifica se há mais resultados e os adiciona
while next_page_token and len(results) < num_results:
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_term}+{location}&key={api_key}&pagetoken={next_page_token}"
    response = requests.get(url)
    results += json.loads(response.text)["results"]
    next_page_token = json.loads(response.text).get("next_page_token")
    # Busca telefone e e-mail de cada local adicionado
    for r in results[len(name):num_results]:
        name.append(r["name"])
        address.append(r["formatted_address"])
        try:
            place_id = r["place_id"]
            # Solicitação para buscar telefone e e-mail
            url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website&key={api_key}"
            response = requests.get(url)
            result = json.loads(response.text)["result"]
            phone.append(result.get("formatted_phone_number", "N/A"))
            email.append(result.get("website", "N/A"))
        except:
            phone.append("N/A")
            email.append("N/A")

# Cria um Pandas DataFrame para armazenar os dados e exporta para um arquivo csv
df = pd.DataFrame({
    "name": name,
    "address": address,
    "phone": phone,
    "email": email
})

df.to_csv("resultado.csv", index=False)
