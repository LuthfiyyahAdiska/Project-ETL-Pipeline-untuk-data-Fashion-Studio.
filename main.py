from utils.extract import scrape_all
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_gsheets, save_to_supabase

def main():
    print("START")

    # EXTRACT
    data = scrape_all()
    print("EXTRACT:", len(data))

    # TRANSFORM
    df = transform_data(data)
    print("TRANSFORM:", len(df))

    # LOAD
    save_to_csv(df)
    save_to_gsheets(df)
    save_to_supabase(df)

    print(df.head())
    print(df.columns)
    print("DONE")

if __name__ == "__main__":
    main()