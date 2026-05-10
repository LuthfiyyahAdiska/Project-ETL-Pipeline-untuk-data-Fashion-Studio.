import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_all():
    base = "https://fashion-studio.dicoding.dev"
    session = requests.Session()
    data = []

    for i in range(1, 51):
        url = f"{base}/page{i}" if i > 1 else base

        try:
            res = session.get(url)
            res.raise_for_status()
        except Exception as e:
            print("Error:", e)
            continue

        soup = BeautifulSoup(res.content, "html.parser")
        cards = soup.find_all("div", class_="collection-card")

        for card in cards:
            try:
                title = card.find("h3", class_="product-title").text.strip()
                price = card.find(class_="price").text.strip()

                p_tags = card.find_all("p")

                rating = next((p.text for p in p_tags if "Rating" in p.text), None)
                colors = next((p.text for p in p_tags if "Colors" in p.text), None)
                size = next((p.text for p in p_tags if "Size" in p.text), None)
                gender = next((p.text for p in p_tags if "Gender" in p.text), None)

                data.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "timestamp": datetime.now()
                })

            except:
                continue

    return data