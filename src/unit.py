import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path so that 'src' can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import DataProcessorBase  # Now this will work

class MockDataProcessor(DataProcessorBase):
    def __init__(self):
        pass  # Override to skip DB loading

class TestDataProcessorBase(unittest.TestCase):

    def setUp(self):
        # Sample data for preprocessing and error calculations
        self.sample_train_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        })

        self.sample_ideal_data = pd.DataFrame({
            'X': [10, 11, 12],
            'Y': [13, 14, 15],
            'Z': [16, 17, 18]
        })

    def test_preprocess_data(self):
        processor = MockDataProcessor()
        processed_data = processor.preprocess_data(self.sample_train_data)
        self.assertIsInstance(processed_data, pd.DataFrame)
        self.assertFalse(processed_data.isnull().values.any())  # Ensure no NaNs

    def test_calculate_squared_errors(self):
        processor = MockDataProcessor()
        errors = processor.calculate_squared_errors([1, 2, 3], [4, 5, 6])
        self.assertEqual(errors, 27)

    def test_find_best_fit_column(self):
        processor = MockDataProcessor()
        normalized_train = processor.preprocess_data(self.sample_train_data)
        normalized_ideal = processor.preprocess_data(self.sample_ideal_data)

        best_fit_indices = processor.find_best_fit_column(normalized_train, normalized_ideal)
        self.assertIsInstance(best_fit_indices, np.ndarray)
        self.assertEqual(len(best_fit_indices), 2)  # 2 train cols compared to 2+ ideal cols

if __name__ == '__main__':
    unittest.main()
