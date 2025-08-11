import requests
import csv

# Função para buscar dados de um Pokémon na API
def buscar_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        
        # Mapeando os campos para o que você quer
        return {
            "nome": dados["name"],                       # Nome do Pokémon
            "altura": dados["height"],                   # Altura
            "idade": dados["base_experience"],           # Usei base_experience como exemplo de "idade"
            "tamanho": dados["weight"]                   # Peso mapeado para tamanho
        }
    else:
        print(f"❌ Não encontrei o Pokémon: {nome}")
        return None

# Lista de Pokémons que vamos buscar
pokemons_lista = ["pikachu", "charmander", "bulbasaur", "squirtle", "eevee"]

# Coletando dados
dados_extraidos = []
for nome in pokemons_lista:
    info = buscar_pokemon(nome)
    if info:
        dados_extraidos.append(info)

# Salvando no CSV — delimitador ponto e vírgula para abrir certo no Excel PT-BR
with open("pokemons.csv", mode="w", newline="", encoding="utf-8") as arquivo:
    colunas = ["nome", "altura", "idade", "tamanho"]
    escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
    escritor.writeheader()
    escritor.writerows(dados_extraidos)

print("✅ Dados extraídos e salvos em 'pokemons.csv'")
