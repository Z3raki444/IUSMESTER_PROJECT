# Importing necessary libraries
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For plotting graphs
from sqlalchemy import create_engine, MetaData  # For interacting with SQL databases

# Base class for data processing
class DataProcessorBase:
    def __init__(self, train_table, ideal_table, test_table, database_url):
        # Load training, ideal, and test data from the database
        self.train_data = self.load_data_from_sql(train_table, database_url)
        self.ideal_data = self.load_data_from_sql(ideal_table, database_url)
        self.test_data = self.load_data_from_sql(test_table, database_url)

    def load_data_from_sql(self, table_name, database_url):
        # Load data from a SQL table
        engine = create_engine(database_url)
        with engine.connect() as conn:
            data = pd.read_sql_table(table_name, conn)
        return data

    def preprocess_data(self, data):
        # Remove missing values and normalize data
        data = data.dropna()
        normalized_data = (data - data.mean()) / data.std()
        return normalized_data

    def calculate_squared_errors(self, column1, column2):
        # Calculate the sum of squared errors between two columns
        if len(column1) != len(column2):
            raise ValueError("Columns must have the same length.")
        squared_errors = (np.array(column1) - np.array(column2))**2
        return np.sum(squared_errors)

    def find_best_fit_column(self, normalized_train, normalized_ideal):
        # Find best-fitting ideal column for each train column based on minimum squared error
        best_fit_indices = []
        for train_col_index in range(1, len(normalized_train.columns)):  # Skip x-column (index 0)
            train_column = normalized_train.iloc[:, train_col_index]
            sum_squared_errors_list = []

            for ideal_col_index in range(1, len(normalized_ideal.columns)):  # Skip x-column
                ideal_column = normalized_ideal.iloc[:, ideal_col_index]
                sum_squared_errors = self.calculate_squared_errors(train_column, ideal_column)
                sum_squared_errors_list.append(round(sum_squared_errors, 5))

            best_fit_index = np.argmin(sum_squared_errors_list)
            best_fit_indices.append(best_fit_index)
        return np.array(best_fit_indices) + 1  # Add 1 to adjust for 1-based indexing

    def plot_data(self, x_axis_range, normalized_ideal, normalized_train, best_fit_indices):
        # Plot the comparison of normalized train and best-matching ideal functions
        for i in range(4):  # Assuming 4 Y-columns in the train data
            plt.title(f'Y{best_fit_indices[i]}')
            plt.plot(x_axis_range, normalized_ideal.iloc[:, best_fit_indices[i]], label='Ideal')
            plt.plot(x_axis_range, normalized_train.iloc[:, i + 1], label='Train')  # i+1 to skip x-column
            plt.legend()
            plt.show()

    def calculate_min_distance(self, array_a, value_b):
        # Calculate the minimum distance between a value and all values in a column
        distances = np.abs(array_a - value_b)
        return np.min(distances)

# Derived class for additional processing, including test classification
class DerivedDataProcessor(DataProcessorBase):
    def __init__(self, train_table, ideal_table, test_table, database_url):
        # Initialize using the parent class and prepare additional variables
        super().__init__(train_table, ideal_table, test_table, database_url)
        self.normalized_train_data = None
        self.normalized_ideal_data = None
        self.normalized_test_data = None
        self.best_fit_indices = None

    def classify_test_data(self, ideal_data_columns):
        # Classify each test value based on closest match to ideal functions
        distances = []
        indices = []

        for _, test_val in self.normalized_test_data.iterrows():
            min_distances = []
            for i in range(4):  # Check against 4 ideal columns
                min_dist = self.calculate_min_distance(ideal_data_columns.iloc[:, i], test_val[1])  # test_val[1] is assumed to be Y value
                min_distances.append(min_dist)

            distances.append(round(min(min_distances), 3))
            indices.append(np.argmin(min_distances))  # Index of closest ideal function

        # Assign labels based on best_fit_indices
        classified_labels = ['Y' + str(self.best_fit_indices[i]) for i in indices]
        return classified_labels, distances

    def main(self):
        # Main workflow for data normalization, fitting, plotting, and classification
        self.normalized_train_data = self.preprocess_data(self.train_data)
        self.normalized_ideal_data = self.preprocess_data(self.ideal_data)
        self.normalized_test_data = self.preprocess_data(self.test_data)

        # Find the best-fitting ideal columns for the train data
        self.best_fit_indices = self.find_best_fit_column(self.normalized_train_data, self.normalized_ideal_data)

        # Plot comparison graphs
        x_axis_range = range(len(self.normalized_train_data))
        self.plot_data(x_axis_range, self.normalized_ideal_data, self.normalized_train_data, self.best_fit_indices)

        # Classify test data points using ideal columns
        classified_labels, deviations = self.classify_test_data(self.normalized_ideal_data.iloc[:, self.best_fit_indices])

        # Create final result DataFrame with classification and deviation
        final_test_data = self.test_data.copy()
        final_test_data["No. of ideal func"] = classified_labels
        final_test_data["Delta Y (test func)"] = deviations
        return final_test_data

# Main program execution
if __name__ == "__main__":
    # Define database connection URL
    database_url = "sqlite:///database.db"

    # Create processor object and run main process
    processor = DerivedDataProcessor("train_table", "ideal_table", "test_table", database_url)
    final_result = processor.main()
    
    # Display the final result
    print(final_result)

    # Store the final result back into the database in a new table called "result"
    engine = create_engine(database_url)
    final_result.to_sql("result", engine, index=False, if_exists="replace")
    print("✔️ Final result loaded into 'result' table in database.db")