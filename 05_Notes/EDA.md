# Exploratory Data Analysis (EDA) Notes

## 1. Basic Information
df.head()
df.tail()
df.shape
df.columns
df.info()
df.describe()

## 2. Missing Values
df.isnull().sum()
df.isnull().mean() * 100

## 3. Duplicate Values
df.duplicated().sum()

## 4. Unique Values
df["column"].unique()
df["column"].nunique()
df["column"].value_counts()

## 5. Filtering

# Equal
df[df["column"] == value]

# Not Equal
df[df["column"] != value]

# AND
df[(condition1) & (condition2)]

# OR
df[(condition1) | (condition2)]

# NOT
df[~(condition)]

# Multiple columns
df.loc[condition, ["col1", "col2"]]

## 6. Data Validation



# Example  Non-smoker but cigarettes > 0
df[(df["currentSmoker"] == 0) & (df["cigsPerDay"] > 0)]

# Example  Smoker but cigarettes = 0
df[(df["currentSmoker"] == 1) & (df["cigsPerDay"] == 0)]




## 7. Grouping
df.groupby("column").mean()
df.groupby("column").count()

## 8. Crosstab
pd.crosstab(df["A"], df["B"])

## 9. Correlation
df.corr(numeric_only=True)

## 10. Outlier Detection
df.boxplot()