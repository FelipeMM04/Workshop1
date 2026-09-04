import sys
from extract import extract_data
from transform import transform_data
from dimensional_model import build_dimensional_model
from load import create_schema, load_data, validate_load


def run_pipeline():
    """Orchestrates the entire ETL pipeline execution following Kimball methodology.

    1. Extract: Reads raw candidate data from CSV.
    2. Transform: Cleans data types and computes business rules ('is_hired').
    3. Dimensional Model: Maps data to Star Schema tables and surrogate keys.
    4. Load: Creates DDL schema, persists tables to MySQL, and validates record counts.
    """
    print("==================================================")
    print("       STARTING ETL PIPELINE - WORKSHOP 1          ")
    print("==================================================")

    # Rutas del Pipeline
    raw_data_path = "data/raw/candidates.csv"

    try:
        # Step 1: Extract
        raw_df = extract_data(raw_data_path)

        # Step 2: Transform (Data Preparation)
        clean_df = transform_data(raw_df)

        # Step 3: Dimensional Modeling
        star_schema_tables = build_dimensional_model(clean_df)

        # Step 4: Load into MySQL Database
        print("\n[STEP 4] Executing Database Load...")
        create_schema()
        load_data()
        validate_load()

        print("\n==================================================")
        print("   ETL PIPELINE EXECUTED SUCCESSFULLY!            ")
        print("==================================================")

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed during execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()