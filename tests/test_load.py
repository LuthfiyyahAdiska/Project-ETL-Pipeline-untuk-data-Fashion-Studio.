import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_gsheets, save_to_supabase


# ==========================================
# TEST save_to_csv
# ==========================================
def test_save_to_csv_success(tmp_path, monkeypatch):
    # Mock getcwd to point to the temporary directory
    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))

    df = pd.DataFrame({"A": [1, 2]})
    result = save_to_csv(df)

    assert result is not None
    assert result.endswith("products.csv")


def test_save_to_csv_error():
    class FakeDF:
        def to_csv(self, *args, **kwargs):
            raise Exception("forced error")

    result = save_to_csv(FakeDF())
    assert result is None


# ==========================================
# TEST save_to_gsheets (mock, tanpa akses real)
# ==========================================
def test_save_to_gsheets_error(monkeypatch):
    """Test bahwa error di Google Sheets ditangani dengan baik."""
    monkeypatch.setattr("os.path.exists", lambda x: False)

    df = pd.DataFrame({"A": [1, 2]})
    result = save_to_gsheets(df)

    assert result is False


# ==========================================
# TEST save_to_supabase (mock, tanpa akses real)
# ==========================================
def test_save_to_supabase_no_key(monkeypatch):
    """Test bahwa tanpa SUPABASE_KEY, fungsi return False."""
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    monkeypatch.setattr("os.path.exists", lambda x: False)

    df = pd.DataFrame({"Title": ["Test"], "Price": [100]})
    result = save_to_supabase(df)

    assert result is False