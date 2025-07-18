# Python Tool for Data Normalization, Matching, and Classification

This project is a Python-based data analysis tool that performs the following tasks:

1. **Reads and imports train, ideal, and test datasets from CSV files into an SQLite database.**
2. **Normalizes the datasets and finds the best matching ideal function for each train function.**
3. **Plots comparison graphs for train and ideal functions.**
4. **Classifies test data points based on the closest ideal function.**
5. **Stores the results back into the database.**
6. **Includes unit tests to validate core functionalities.**

---

## 📂 Project Structure

.
├── datasets/
│ ├── train.csv
│ ├── ideal.csv
│ └── test.csv
├── src/
│ ├── main.py # Contains DataProcessorBase and DerivedDataProcessor classes
├── tests/
│ ├── test_main.py # Unit tests using unittest
├── database.db # SQLite database file
├── plot_1.png # Comparison plot (e.g., Y1)
├── plot_2.png # Comparison plot (e.g., Y11)
├── plot_4.png # Comparison plot (e.g., Y31)
└── README.md # This file

yaml
Copy
Edit

---

## 🚀 How It Works

### Step 1: Load Data into SQLite

CSV files from the `datasets/` folder are loaded into the `database.db` SQLite database using SQLAlchemy.

df.to_sql(table_name, engine, index=False, if_exists="replace")

Step 2: Normalize Data
Data is normalized using Z-score normalization (zero mean, unit variance):
normalized_data = (data - data.mean()) / data.std()

Step 3: Match Train Functions to Ideal Functions
The ideal function with the minimum sum of squared errors (SSE) is selected for each train function.

Step 4: Plot Data
Plots are generated comparing each normalized train function to its closest ideal match using Matplotlib.

Step 5: Classify Test Data
Each test data point is classified to the closest ideal function by minimum absolute Y-difference.

Step 6: Save Results
The results are saved into the database in a table named result.

🧪 Running Tests
Tests are located in the tests/ folder. You can run them with:

python -m unittest tests/test_main.py
The tests cover:

Data normalization
Squared error calculations
Best-fit function identification

📦 Requirements
Python 3.7+
pandas
numpy
matplotlib
SQLAlchemy

Install dependencies using:
pip install -r requirements.txt
(You may need to create the requirements.txt with the above libraries.)

🏁 Running the Project
From the root directory:

python src/main.py
This will:

Normalize data
Match train to ideal functions
Classify test data
Save results to SQLite
Display plots

🛠 Future Improvements
Add GUI using Tkinter or Streamlit

Export results to CSV
Handle edge cases in data classification
Improve performance on large datasets

👨‍💻 Author
Preveenkumar Muthukumar
Project for IU Germany – MSc Computer Science course on Python Programming

