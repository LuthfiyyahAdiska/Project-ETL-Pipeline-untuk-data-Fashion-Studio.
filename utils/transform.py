import pandas as pd


def transform_data(data):
    df = pd.DataFrame(data)

    # Hapus produk tidak valid
    df = df[df["Title"] != "Unknown Product"]

    # Hapus price tidak valid
    df = df[~df["Price"].isin(["Price Unavailable", None])]

    # Convert price ke rupiah
    df["Price"] = df["Price"].str.replace("$", "", regex=False).astype(float) * 16000

    # Hapus rating invalid
    df = df[~df["Rating"].isin([
        "Rating: Not Rated",
        "Rating: ⭐ Invalid Rating / 5"
    ])]

    # Ambil angka rating
    df["Rating"] = df["Rating"].str.extract(r"(\d+\.\d+)").astype(float)

    # Colors jadi angka
    df["Colors"] = df["Colors"].str.extract(r"(\d+)").astype(int)

    # Bersihin Size & Gender
    df["Size"] = df["Size"].str.replace("Size:", "").str.strip()
    df["Gender"] = df["Gender"].str.replace("Gender:", "").str.strip()

    # Bersihin final
    df = df.dropna().drop_duplicates()

    return df