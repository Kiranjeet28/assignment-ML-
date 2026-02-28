import os
import pandas as pd
from functools import lru_cache

# Resolve path relative to this file so it works regardless of CWD
_DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "..", "titanic.csv")


@lru_cache(maxsize=1)
def load_titanic_dataset(csv_path: str = _DEFAULT_CSV) -> pd.DataFrame:
    """
    Load and cache the Titanic dataset.
    The @lru_cache ensures the CSV is read from disk only once per process.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Titanic CSV not found at: {csv_path}\n"
            "Run setup_project.py to download it."
        )
    df = pd.read_csv(csv_path)
    return df