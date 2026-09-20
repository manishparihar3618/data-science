# Support Vector Machine (SVM) Classification

A practical implementation of **SVM classification using Scikit-learn**, focused on understanding core concepts and hyperparameter tuning.

## Concepts Covered

* SVM & SVC
* Linear & Non-linear Classification
* Kernel Functions
* Feature Scaling
* `C` & `Gamma` Tuning
* GridSearchCV
* Cross-Validation
* Model Evaluation
* Underfitting & Overfitting

## Workflow

```text
Data → Preprocessing → Scaling → SVC
     → Kernel Selection → C/Gamma Tuning
     → GridSearchCV → Evaluation
```

## Tech Stack

Python • Pandas • NumPy • Matplotlib • Scikit-learn

## Datasets

* Breast Cancer Dataset
* Wine Dataset
* Synthetic Classification Datasets

## Key Learning

Explored how **kernels, C, gamma, scaling, and cross-validation** affect SVM performance and model generalization.


### Defination 
Support Vector Machine is a supervised machine learning algorithm primarily used for classification. It finds an optimal hyperplane that separates classes while maximizing the margin between them. The training points closest to the decision boundary are called support vectors and play a key role in determining the hyperplane. For non-linearly separable data, SVM can use kernel functions such as linear, polynomial, RBF, and sigmoid to construct nonlinear decision boundaries. In soft-margin SVM, the parameter C controls the penalty for margin violations, while gamma, particularly with the RBF kernel, controls the influence of individual training points. Since SVM is sensitive to feature scale, feature scaling is generally recommended. SVM can also be extended to regression, known as Support Vector Regression (SVR).