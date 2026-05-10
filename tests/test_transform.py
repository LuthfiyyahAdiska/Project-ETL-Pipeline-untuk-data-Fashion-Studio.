import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import transform_data

def test_transform_valid():
    data = [{
        "Title": "T-shirt",
        "Price": "$10.00",
        "Rating": "Rating: ⭐ 4.5 / 5",
        "Colors": "3 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Men",
        "timestamp": "2025"
    }]

    df = transform_data(data)

    assert not df.empty
    assert df.iloc[0]["Price"] == 160000
    assert df.iloc[0]["Rating"] == 4.5
    assert df.iloc[0]["Colors"] == 3