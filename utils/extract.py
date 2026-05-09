import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def scrape_fashion_studio():
    base_url = "https://fashion-studio.dicoding.dev"
    max_pages = 50  
    all_products = []

    logging.info("Mulai melakukan ekstraksi data...")

    for page in range(1, max_pages + 1):
        url = f"{base_url}/?page={page}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            product_cards = soup.find_all('div', class_='collection-card') 
            
            for card in product_cards:
                try:

                    title_elem = card.find('h3', class_='product-title')
                    title = title_elem.text.strip() if title_elem else None
                    
                    price_elem = card.find('div', class_='price-container')
                    price = price_elem.text.strip() if price_elem else None
                    
                    p_tags = card.find_all('p')
                    
                    rating = None
                    colors = None
                    size = None
                    gender = None
                    
                    if len(p_tags) >= 4:
                        rating = p_tags[0].text.strip()
                        colors = p_tags[1].text.strip()
                        size = p_tags[2].text.strip()
                        gender = p_tags[3].text.strip()
                    
                    all_products.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender
                    })
                except Exception as e:
                    logging.warning(f"Gagal mengambil elemen produk di halaman {page}: {e}")
                    continue
                    
        except requests.exceptions.RequestException as e:
            logging.error(f"Gagal mengakses halaman {page}. Error: {e}")
            continue 

    df_raw = pd.DataFrame(all_products)
    return df_raw