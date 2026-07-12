# Pickling in Machine Learning

## What is Pickling?

Pickling is the process of saving a trained machine learning model to a file so that it can be loaded later without training it again.

---

## Why do we use Pickle?

Training a machine learning model can take a long time, especially on large datasets. Instead of retraining the model every time we want to make predictions, we save the trained model using Pickle.

---

## Example

Suppose we have a dataset of *10,000 records* containing:

| Height | Weight |
|--------|--------|
|170|65|
|180|75|
|...|...|

### Step 1: Train the model

python
model.fit(X_train, y_train)


The model learns the relationship between *Height → Weight*.

---

### Step 2: Save the trained model

python
import pickle

pickle.dump(model, open("model.pkl", "wb"))


This creates a file named *model.pkl* containing everything the model has learned.

---

### Step 3: Load the model later

python
model = pickle.load(open("model.pkl", "rb"))


No retraining is required.

---

### Step 4: Predict new data

Suppose a new person has:

- Height = *175 cm*

python
prediction = model.predict([[175]])


Output:


Predicted Weight = 69.8 kg


The model directly predicts the weight using the knowledge learned from the original 10,000 records.

---

## Without Pickle

Every time you restart your program, you must:

1. Load the dataset.
2. Train the model again.
3. Then make predictions.

This wastes time and computational resources.

---

## With Pickle

1. Train the model only once.
2. Save it using Pickle.
3. Load the saved model whenever needed.
4. Make predictions instantly.

---

## Real-World Use Case

Suppose you build a *House Price Prediction* website.

When a user enters house details:

- ❌ The website should NOT train the model every time.
- ✅ It simply loads the saved *model.pkl* file and predicts the house price in seconds.

This is how most Machine Learning models are deployed in production.

---

## Key Points

- fit() → Trains the model.
- pickle.dump() → Saves the trained model.
- pickle.load() → Loads the saved model.
- predict() → Makes predictions using the loaded model.
- Pickle *does not improve accuracy*; it simply avoids retraining the model.

---

## One-Line Definition

> *Pickle is used to save a trained machine learning model so it can be loaded later and used for prediction without training it again.*