# Built-in Datasets in Scikit-learn

## Why is this a new concept?

Until now, I was loading datasets from CSV files using Pandas.

Example:

python
import pandas as pd

df = pd.read_csv("housing.csv")


Here, the data already exists in a CSV file.

---

## What is different now?

Scikit-learn provides some datasets directly through Python.

Example:

python
from sklearn.datasets import fetch_california_housing

dataset = fetch_california_housing()


No CSV file is required.

The dataset is returned as a *Bunch object*, which stores both the data and useful metadata.

---

## What does the dataset contain?

- dataset.data → Feature values
- dataset.target → Target column
- dataset.feature_names → Feature names
- dataset.target_names → Target variable name
- dataset.DESCR → Complete dataset description

---

## Why use built-in datasets?

- No need to download CSV files.
- Standard datasets for learning and practice.
- Same dataset is available to every user.
- Useful for testing ML algorithms quickly.

---

## Converting into a DataFrame

python
import pandas as pd

df = pd.DataFrame(dataset.data, columns=dataset.feature_names)
df["Target"] = dataset.target


Now the data is ready for:

- Exploratory Data Analysis (EDA)
- Feature Engineering
- Machine Learning
- Model Evaluation

---

## Different Ways to Get Data in Machine Learning

1. CSV files → pd.read_csv()
2. Excel files → pd.read_excel()
3. SQL Databases → SQL queries
4. APIs → requests.get()
5. Web Scraping → BeautifulSoup
6. Built-in Scikit-learn datasets → fetch_california_housing(), load_iris(), etc.

---

## Key Takeaway

The source of the data may change, but after converting it into a Pandas DataFrame, the Machine Learning workflow remains the same.


Get Data
      ↓
Create DataFrame
      ↓
EDA
      ↓
Feature Engineering
      ↓
Train-Test Split
      ↓
Model Training
      ↓
Evaluation