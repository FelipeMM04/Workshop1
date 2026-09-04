import os
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text

# Configuración de la base de datos
DB_USER = "root"
DB_PASS = "ADsemestre2025" 
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "kimball_dw"

connection_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sa.create_engine(connection_url)

def create_schema():
    """Crea las tablas DDL con Primary Keys y Foreign Keys en MySQL."""
    ddl_statements = [
        # 1. Borrar tablas si existen (en orden inverso de dependencias)
        "DROP TABLE IF EXISTS fact_candidate_evaluations;",
        "DROP TABLE IF EXISTS dim_candidate;",
        "DROP TABLE IF EXISTS dim_technology;",
        "DROP TABLE IF EXISTS dim_location;",
        "DROP TABLE IF EXISTS dim_date;",

        # 2. Crear dim_candidate
        """
        CREATE TABLE dim_candidate (
            candidate_sk INT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(255)
        );
        """,

        # 3. Crear dim_technology
        """
        CREATE TABLE dim_technology (
            technology_sk INT PRIMARY KEY,
            technology_name VARCHAR(100),
            seniority VARCHAR(50)
        );
        """,

        # 4. Crear dim_location
        """
        CREATE TABLE dim_location (
            location_sk INT PRIMARY KEY,
            country VARCHAR(100)
        );
        """,

        # 5. Crear dim_date
        """
        CREATE TABLE dim_date (
            date_sk INT PRIMARY KEY,
            full_date DATE,
            year INT,
            month INT,
            day INT,
            quarter INT
        );
        """,

        # 6. Crear fact_candidate_evaluations con Foreign Keys
        """
        CREATE TABLE fact_candidate_evaluations (
            evaluation_id INT AUTO_INCREMENT PRIMARY KEY,
            candidate_sk INT,
            technology_sk INT,
            location_sk INT,
            application_date_sk INT,
            years_of_experience INT,
            code_challenge_score INT,
            technical_interview_score INT,
            is_hired TINYINT(1),
            FOREIGN KEY (candidate_sk) REFERENCES dim_candidate(candidate_sk),
            FOREIGN KEY (technology_sk) REFERENCES dim_technology(technology_sk),
            FOREIGN KEY (location_sk) REFERENCES dim_location(location_sk),
            FOREIGN KEY (application_date_sk) REFERENCES dim_date(date_sk)
        );
        """
    ]

    with engine.connect() as conn:
        for stmt in ddl_statements:
            conn.execute(text(stmt))
        conn.commit()
    print("✓ Esquema de tablas (DDL) creado correctamente en MySQL.")

def load_data():
    """Carga los archivos CSV a la base de datos MySQL en orden estricto."""
    processed_dir = "data/processed"

    # Cargar Dimensiones
    print("Cargando dimensiones...")
    dim_candidate = pd.read_csv(os.path.join(processed_dir, "dim_candidate.csv"))
    dim_technology = pd.read_csv(os.path.join(processed_dir, "dim_technology.csv"))
    dim_location = pd.read_csv(os.path.join(processed_dir, "dim_location.csv"))
    dim_date = pd.read_csv(os.path.join(processed_dir, "dim_date.csv"))

    dim_candidate.to_sql("dim_candidate", con=engine, if_exists="append", index=False)
    dim_technology.to_sql("dim_technology", con=engine, if_exists="append", index=False)
    dim_location.to_sql("dim_location", con=engine, if_exists="append", index=False)
    dim_date.to_sql("dim_date", con=engine, if_exists="append", index=False)
    print("✓ Dimensiones cargadas con éxito.")

    # Cargar Fact Table
    print("Cargando Fact Table...")
    fact_df = pd.read_csv(os.path.join(processed_dir, "fact_candidate_evaluations.csv"))
    fact_df.to_sql("fact_candidate_evaluations", con=engine, if_exists="append", index=False)
    print("✓ Fact Table cargada con éxito.")

def validate_load():
    """Valida los conteos de registros cargados en la base de datos."""
    print("\n--- Validación de Registros en MySQL ---")
    tables = [
        "dim_candidate",
        "dim_technology",
        "dim_location",
        "dim_date",
        "fact_candidate_evaluations"
    ]
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table};"))
            count = result.scalar()
            print(f"Tabla `{table}`: {count:,} registros")

if __name__ == "__main__":
    create_schema()
    load_data()
    validate_load()