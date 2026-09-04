import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepares and transforms raw candidate data according to analytical requirements.

    - Standardizes column names.
    - Handles duplicated records and missing values.
    - Converts data types (dates to datetime).
    - Derives the 'is_hired' target binary flag based on business rules.
    """
    print("--- [ETL: TRANSFORM] Starting Data Preparation ---")

    # 1. Copia de trabajo para evitar alterar la referencia original
    df_clean = df.copy()

    # 2. Manejo de Registros Duplicados
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    deduped_rows = len(df_clean)
    if initial_rows - deduped_rows > 0:
        print(f"Removed {initial_rows - deduped_rows} duplicate rows.")

    # 3. Normalización de Tipos de Datos (Fechas)
    df_clean["Application Date"] = pd.to_datetime(df_clean["Application Date"])

    # 4. Manejo de Valores Faltantes (Valores Nulos)
    # Rellenar o verificar que los atributos clave no contengan nulos
    df_clean["YOE"] = df_clean["YOE"].fillna(0).astype(int)
    df_clean["Code Challenge Score"] = df_clean["Code Challenge Score"].fillna(0).astype(int)
    df_clean["Technical Interview Score"] = df_clean["Technical Interview Score"].fillna(0).astype(int)

    # 5. Derivación de Regla de Negocio: 'is_hired'
    # Hired (1) si Code Challenge >= 7 Y Technical Interview >= 7, de lo contrario (0)
    df_clean["is_hired"] = (
        (df_clean["Code Challenge Score"] >= 7)
        & (df_clean["Technical Interview Score"] >= 7)
    ).astype(int)

    print(
        f"Data preparation complete: {len(df_clean)} records processed. Total hired candidates: {df_clean['is_hired'].sum()}"
    )

    return df_clean


if __name__ == "__main__":
    from extract import extract_data

    # Prueba local del módulo de transformación
    raw_df = extract_data("data/raw/candidates.csv")
    clean_df = transform_data(raw_df)

    print("\nProcessed DataFrame summary:")
    print(clean_df.info())