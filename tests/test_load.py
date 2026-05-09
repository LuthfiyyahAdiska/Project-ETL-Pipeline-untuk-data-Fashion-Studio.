import unittest
from utils.load import save_to_csv

class TestLoad(unittest.TestCase):
    def test_save_to_csv_exists(self):
        self.assertTrue(callable(save_to_csv))

if __name__ == '__main__':
    unittest.main()