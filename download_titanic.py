# This script downloads the Titanic dataset from Kaggle using kagglehub and saves it as titanic.csv in the project root.
# Usage: python download_titanic.py

import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load from the Kaggle dataset
target_file = "train.csv"  # or "titanic.csv" if that's the file in the dataset

# Load the latest version of the dataset as a pandas DataFrame
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "yasserh/titanic-dataset",
    target_file,
)

# Save as titanic.csv in the project root
df.to_csv("../titanic.csv", index=False)
print("Saved Titanic dataset as titanic.csv")
