import os
import pandas as pd


def extract_data(file_path: str = "data/raw/candidates.csv") -> pd.DataFrame:
    """Reads the raw candidates CSV source data into a Pandas DataFrame.

    Preserves the original source file without performing any business logic or
    transformations. Uses ';' as the column separator.
    """
    print("--- [ETL: EXTRACT] Reading source dataset ---")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Error: Raw file not found at path: {file_path}"
        )

    # Se especifica sep=";" para separar correctamente las columnas
    df = pd.read_csv(file_path, sep=";")

    print(
        f"Successfully loaded {len(df)} records from '{file_path}' with {len(df.columns)} columns."
    )
    return df


if __name__ == "__main__":
    raw_df = extract_data("data/raw/candidates.csv")
    print("\nColumns detected:", list(raw_df.columns))
    print("\nFirst 3 rows of raw extracted data:")
    print(raw_df.head(3))