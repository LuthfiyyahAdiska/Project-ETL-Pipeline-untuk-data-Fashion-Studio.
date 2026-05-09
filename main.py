from utils.extract import scrape_fashion_studio
from utils.transform import clean_data
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql

def main():
    raw_data = scrape_fashion_studio()
    cleaned_data = clean_data(raw_data)

    print("\n[3/3] Sedang menyimpan data...")
    
    save_to_csv(cleaned_data, 'products.csv')
    
    SPREADSHEET_ID = '1DpF-uYjNgLxrR3czssjIsp2-Yu0GVHMC0zqzjnyQVXE' 
    save_to_google_sheets(cleaned_data, SPREADSHEET_ID)
    
    DB_URI = 'postgresql://postgres.klogkmvbkexijcjchflx:3tlf4510nluthf1yy4@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres'
    save_to_postgresql(cleaned_data, DB_URI)
    
    print("\n=== ✨ Proses ETL Pipeline Selesai! ✨ ===")

if __name__ == "__main__":
    main()