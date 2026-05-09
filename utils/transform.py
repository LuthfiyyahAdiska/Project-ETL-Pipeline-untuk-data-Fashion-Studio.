import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def clean_data(df):
    logging.info("Memulai proses transformasi (pembersihan) data...")
    
    try:
        df_clean = df.dropna().drop_duplicates().copy()
        
        df_clean = df_clean[df_clean['Title'] != 'Unknown Product']
        df_clean = df_clean[~df_clean['Rating'].str.contains('Invalid', na=False)]
        
        df_clean['Price'] = df_clean['Price'].str.replace('$', '', regex=False).astype(float)
        df_clean['Price'] = df_clean['Price'] * 16000
        
        df_clean['Rating'] = df_clean['Rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
        
        df_clean['Colors'] = df_clean['Colors'].str.extract(r'(\d+)').astype(int)
        
        df_clean['Size'] = df_clean['Size'].str.replace('Size: ', '', regex=False).str.strip()
        
        df_clean['Gender'] = df_clean['Gender'].str.replace('Gender: ', '', regex=False).str.strip()
        
        df_clean['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        df_clean.reset_index(drop=True, inplace=True)
        
        return df_clean

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat transformasi: {e}")
        return None