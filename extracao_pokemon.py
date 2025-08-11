import requests
import csv
import time
import matplotlib.pyplot as plt

# Função para buscar dados de um Pokémon na API
def buscar_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    
    try:
        resposta = requests.get(url, timeout=10)  # timeout evita travar
        resposta.raise_for_status()  # levanta erro se status != 200
        
        dados = resposta.json()

        return {
            "nome": dados["name"],
            "altura": dados["height"],
            "idade": dados["base_experience"],  # exemplo para "idade"
            "tamanho": dados["weight"]
        }
    except requests.exceptions.HTTPError:
        print(f"❌ Pokémon '{nome}' não encontrado (erro HTTP).")
    except requests.exceptions.Timeout:
        print(f"⏳ Tempo de espera excedido para '{nome}'.")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao buscar '{nome}': {e}")
    return None

# Lista de Pokémons para buscar
pokemons_lista = ["pikachu", "charmander", "bulbasaur", "squirtle", "eevee"]

# Coletando dados com pequena pausa para não sobrecarregar API
dados_extraidos = []
for nome in pokemons_lista:
    info = buscar_pokemon(nome)
    if info:
        dados_extraidos.append(info)
    time.sleep(0.5)  # pausa de meio segundo

# Salvando no CSV
if dados_extraidos:
    with open("pokemons.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        colunas = ["nome", "altura", "idade", "tamanho"]
        escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
        escritor.writeheader()
        escritor.writerows(dados_extraidos)
    print("✅ Dados extraídos e salvos em 'pokemons.csv'.")

    # Criar gráfico (altura x tamanho)
    nomes = [p["nome"] for p in dados_extraidos]
    alturas = [p["altura"] for p in dados_extraidos]
    tamanhos = [p["tamanho"] for p in dados_extraidos]

    plt.figure(figsize=(8, 5))
    plt.bar(nomes, alturas, color="skyblue", label="Altura")
    plt.plot(nomes, tamanhos, color="red", marker="o", label="Tamanho")
    plt.xlabel("Pokémon")
    plt.ylabel("Valores")
    plt.title("Altura e Tamanho dos Pokémons")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafico_pokemons.png")
    print("📊 Gráfico salvo em 'grafico_pokemons.png'.")
else:
    print("⚠️ Nenhum dado foi extraído.")
