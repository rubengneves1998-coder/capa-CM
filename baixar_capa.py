import requests
from bs4 import BeautifulSoup

url = "https://www.vercapas.com/capa/correio-da-manha.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Procurar a imagem da capa: começa por https://imgs.vercapas.com/covers/correio-da-manha/
capa = soup.find("img", src=lambda s: s and "imgs.vercapas.com/covers/correio-da-manha" in s)

if capa:
    img_url = capa["src"]
    img_data = requests.get(img_url, headers=headers).content
    with open("correio-capa.jpg", "wb") as f:
        f.write(img_data)
    print("✅ Capa salva como correio-capa.jpg:", img_url)
else:
    print("⚠️ Não encontrei a capa do jornal.")

