import pandas as pd

def load_titanic_data(filepath='titanic.csv'):
    """
    Loads the Titanic dataset from a CSV file into a Pandas DataFrame.
    Args:
        filepath (str): Path to the Titanic CSV file.
    Returns:
        pd.DataFrame: DataFrame containing the Titanic data.
    """
    df = pd.read_csv(filepath)
    return df

# Example usage:
if __name__ == "__main__":
    df = load_titanic_data()
    print(df.head())
