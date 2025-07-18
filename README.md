# Python Tool for Data Normalization, Matching, and Classification

A Python-based data analysis tool that automates the normalization, matching, classification, and visualization of datasets, integrated with SQLite for efficient data management.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [How It Works](#how-it-works)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Testing](#testing)  
- [Future Improvements](#future-improvements)  
- [Author](#author)  

---

## Overview

This tool reads train, ideal, and test datasets from CSV files, normalizes the data, matches train functions with ideal functions based on minimum error, classifies test data points, visualizes the results, and stores everything in an SQLite database.

---

## Features

- Load CSV datasets into SQLite using SQLAlchemy  
- Z-score normalization of datasets  
- Match train functions to ideal functions by minimizing sum of squared errors  
- Classify test data based on closest ideal function  
- Visualization of train vs ideal functions using Matplotlib  
- Store classification results back into the database  
- Unit tests for core functionality  

---

## How It Works

1. **Load Data**  
   Import CSV files into SQLite tables.

2. **Normalize Data**  
   Apply Z-score normalization for standardized comparison.

3. **Match Functions**  
   Identify the ideal function best matching each train function by minimizing squared error.

4. **Plot Data**  
   Generate comparison plots of train and ideal functions.

5. **Classify Test Data**  
   Assign test points to the closest ideal function based on minimal Y-value difference.

6. **Save Results**  
   Persist classification results in the SQLite `result` table.

---

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the main script to execute the full pipeline:

```bash
python src/main.py
