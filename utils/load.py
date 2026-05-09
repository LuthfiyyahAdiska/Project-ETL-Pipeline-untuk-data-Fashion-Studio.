import logging
import gspread
from sqlalchemy import create_engine 

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def save_to_csv(df, file_name="products.csv"):
    try:
        df.to_csv(file_name, index=False)
        logging.info("✅ Data berhasil disimpan ke format CSV!")
    except Exception as e:
        logging.error(f"❌ Gagal menyimpan data ke CSV: {e}")

def save_to_google_sheets(df, spreadsheet_id):
    try:
        gc = gspread.service_account(filename='google-sheets-api.json')
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.sheet1
        worksheet.clear()
        data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(data_to_upload)
        logging.info("✅ Data berhasil disimpan ke Google Sheets!")
    except Exception as e:
        logging.error(f"❌ Gagal menyimpan data ke Google Sheets: {e}")

def save_to_postgresql(df, connection_uri):
    logging.info("Memulai proses penyimpanan data ke PostgreSQL (Supabase)...")
    try:
        engine = create_engine(connection_uri)
        df.to_sql('fashion_products', engine, if_exists='replace', index=False)
        logging.info("✅ Data berhasil disimpan ke PostgreSQL!")
    except Exception as e:
        logging.error(f"❌ Gagal menyimpan data ke PostgreSQL: {e}")