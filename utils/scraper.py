import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

urls = [
    "https://www.worldometers.info/geography/flags-of-the-world/",
    "https://www.worldometers.info/geography/flags-of-dependent-territories/",
]
headers = {"User-Agent": "Mozilla/5.0"}

os.makedirs("flags", exist_ok=True)


for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    for a_tag in soup.find_all("a"):
        img_tag = a_tag.find("img")
        if img_tag and a_tag.get("href"):
            file_url = urljoin(url, a_tag["href"])
            alt_text = img_tag.get("alt", "file")

            parsed = urlparse(file_url)
            ext = os.path.splitext(parsed.path)[-1]

            filename = f"{alt_text}{ext}"
            filepath = os.path.join("flags", filename)

            file_response = requests.get(file_url, headers=headers)
            if file_response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(file_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed: {file_url} ({file_response.status_code})")
