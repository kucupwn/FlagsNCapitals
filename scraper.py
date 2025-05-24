import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.worldometers.info/geography/flags-of-the-world/"
headers = {"User-Agent": "Mozilla/5.0"}

os.makedirs("images", exist_ok=True)

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
