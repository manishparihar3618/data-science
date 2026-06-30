## Data Leakage

Definition:
Data leakage occurs when information unavailable at prediction time is used to train the model.

Effects:
- Artificially high accuracy
- Unrealistic performance
- Poor real-world generalization

Common Causes:
1. Future information
2. Target-related columns
3. IDs encoding the target
4. Preprocessing before train-test split
5. Target leakage during feature engineering

How to Detect:
- Suspiciously high accuracy (99–100%)
- Extremely high feature correlation
- One feature dominating importance
- Performance drops on new data

Prevention:
- Understand every feature
- Remove future information
- Split data before preprocessing
- Validate on unseen data
- Review features with domain knowledge


# Example: Student Pass Prediction

Target: Pass / Fail

Features:
- ✅ Study Hours
- ✅ Attendance
- ❌ Final Marks

Why is *Final Marks* wrong?

Because Final Marks determine whether the student passes. The model already sees the answer, so it gives unrealistically high accuracy.

In real life, Final Marks are not available before the exam.

This is called *Data Leakage*.

*Rule:* Keep only those features that are available at prediction time.