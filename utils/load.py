import os
import requests as http_requests
import gspread
from google.oauth2.service_account import Credentials


# ==========================================
# 1. SAVE TO CSV
# ==========================================
def save_to_csv(df):
    """Menyimpan DataFrame ke file CSV."""
    try:
        path = os.path.join(os.getcwd(), "products.csv")
        df.to_csv(path, index=False)
        print("Saved CSV:", path)
        return path
    except Exception as e:
        print("Error saving CSV:", e)
        return None


# ==========================================
# 2. SAVE TO GOOGLE SHEETS
# ==========================================
def save_to_gsheets(df):
    """Upload DataFrame ke Google Sheets menggunakan Service Account."""
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        SPREADSHEET_ID = "1DpF-uYjNgLxrR3czssjIsp2-Yu0GVHMC0zqzjnyQVXE"

        # Cari credential file
        cred_file = os.path.join(os.getcwd(), "google-sheets-api.json")
        if not os.path.exists(cred_file):
            cred_file = os.path.join(os.getcwd(), "etl-submission-pemda-b82b806d5816.json")

        creds = Credentials.from_service_account_file(cred_file, scopes=SCOPES)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(SPREADSHEET_ID).sheet1

        # Clear data lama, lalu isi ulang
        sheet.clear()

        # Header + data (convert semua ke string agar serializable)
        header = df.columns.tolist()
        rows = df.astype(str).values.tolist()

        sheet.update([header] + rows)

        print("Saved to Google Sheets!")
        return True
    except Exception as e:
        print("Error saving to Google Sheets:", e)
        return False


# ==========================================
# 3. SAVE TO SUPABASE (REST API)
# ==========================================
def save_to_supabase(df):
    """Upload DataFrame ke Supabase via REST API."""
    try:
        SUPABASE_URL = "https://klogkmvbkexijcjchflx.supabase.co"
        SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

        # Jika key tidak ada di env, coba baca dari file .env
        if not SUPABASE_KEY:
            env_path = os.path.join(os.getcwd(), ".env")
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        if line.startswith("SUPABASE_KEY="):
                            SUPABASE_KEY = line.strip().split("=", 1)[1]

        if not SUPABASE_KEY:
            print("Error: SUPABASE_KEY tidak ditemukan. Set di .env atau environment variable.")
            return False

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        # Hapus data lama
        http_requests.delete(
            f"{SUPABASE_URL}/rest/v1/fashion_products",
            headers={**headers, "Prefer": "return=minimal"},
            params={"Title": "neq.IMPOSSIBLE_VALUE_THAT_DOESNT_EXIST"}
        )

        # Siapkan records
        records = df.to_dict(orient="records")
        for r in records:
            for key, val in r.items():
                if hasattr(val, 'isoformat'):
                    r[key] = val.isoformat()

        # Insert batch (kirim per 500 baris agar tidak timeout)
        batch_size = 500
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            response = http_requests.post(
                f"{SUPABASE_URL}/rest/v1/fashion_products",
                headers=headers,
                json=batch
            )
            response.raise_for_status()

        print(f"Saved {len(df)} rows to Supabase!")
        return True
    except Exception as e:
        print("Error saving to Supabase:", e)
        return False