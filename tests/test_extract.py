import unittest
from utils.extract import scrape_fashion_studio
import pandas as pd

class TestExtract(unittest.TestCase):
    def test_scrape_output_type(self):
        
        data = scrape_fashion_studio()
        self.assertIsInstance(data, pd.DataFrame)
        
    def test_scrape_not_empty(self):
        
        data = scrape_fashion_studio()
        self.assertFalse(data.empty)

if __name__ == '__main__':
    unittest.main()