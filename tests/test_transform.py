import unittest
import pandas as pd
from utils.transform import clean_data

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.raw_data = pd.DataFrame({
            'Title': ['T-shirt 1', 'Unknown Product'],
            'Price': ['$10.0', '$20.0'],
            'Rating': ['Rating: 4.5 / 5', 'Invalid Rating'],
            'Colors': ['3 Colors', '1 Color'],
            'Size': ['Size: M', 'Size: L'],
            'Gender': ['Gender: Men', 'Gender: Women']
        })

    def test_clean_data_output(self):
        result = clean_data(self.raw_data)
        
        self.assertEqual(len(result), 1)
        
        self.assertEqual(result['Price'].iloc[0], 160000.0)
        
        self.assertEqual(result['Size'].iloc[0], 'M')
        
        self.assertIn('timestamp', result.columns)

if __name__ == '__main__':
    unittest.main()