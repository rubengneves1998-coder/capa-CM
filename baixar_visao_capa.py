import requests
from bs4 import BeautifulSoup
import os
import hashlib
import sys

file_path = os.path.join(os.getcwd(), "visao-capa.jpg")

url = "https://www.vercapas.com/capa/visao.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ Erro ao baixar a página: {e}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")
capa = soup.find("img", src=lambda s: s and "imgs.vercapas.com/covers/visao" in s)

if not capa:
    print("⚠️ Não encontrei a capa da Visão.")
    sys.exit(0)

img_url = capa["src"]
print("✅ URL da capa encontrada:", img_url)

try:
    img_response = requests.get(img_url, headers=headers, timeout=15)
    img_response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ Erro ao baixar a imagem: {e}")
    sys.exit(1)

img_data = img_response.content

def file_hash(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

old_hash = file_hash(file_path)
new_hash = hashlib.sha256(img_data).hexdigest()

if old_hash == new_hash:
    print("⚠️ A imagem é igual à anterior. Nenhuma atualização necessária.")
else:
    with open(file_path, "wb") as f:
        f.write(img_data)
    print("✅ Nova capa da Visão salva:", file_path)
