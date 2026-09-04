import pandas as pd


def build_dimensional_model(df: pd.DataFrame) -> dict:
    """Transforms prepared flat data into Kimball Star Schema DataFrames:

    - dim_candidate
    - dim_technology
    - dim_location
    - dim_date
    - fact_candidate_evaluations
    """
    print(
        "\n--- [ETL: DIMENSIONAL MODELING] Building Star Schema Tables ---"
    )

    # 1. Dimensión Candidato
    dim_candidate = (
        df[["First Name", "Last Name", "Email"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_candidate["candidate_sk"] = dim_candidate.index + 1
    dim_candidate.rename(
        columns={
            "First Name": "first_name",
            "Last Name": "last_name",
            "Email": "email",
        },
        inplace=True,
    )
    dim_candidate = dim_candidate[
        ["candidate_sk", "first_name", "last_name", "email"]
    ]

    # 2. Dimensión Tecnología
    dim_technology = (
        df[["Technology", "Seniority"]].drop_duplicates().reset_index(drop=True)
    )
    dim_technology["technology_sk"] = dim_technology.index + 1
    dim_technology.rename(
        columns={"Technology": "technology_name", "Seniority": "seniority"},
        inplace=True,
    )
    dim_technology = dim_technology[
        ["technology_sk", "technology_name", "seniority"]
    ]

    # 3. Dimensión Ubicación
    dim_location = (
        df[["Country"]].drop_duplicates().reset_index(drop=True)
    )
    dim_location["location_sk"] = dim_location.index + 1
    dim_location.rename(columns={"Country": "country"}, inplace=True)
    dim_location = dim_location[["location_sk", "country"]]

    # 4. Dimensión Fecha
    unique_dates = pd.DataFrame(
        {"full_date": df["Application Date"].drop_duplicates()}
    )
    dim_date = pd.DataFrame()
    dim_date["full_date"] = unique_dates["full_date"]
    dim_date["date_sk"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date = dim_date[
        ["date_sk", "full_date", "year", "month", "day", "quarter"]
    ].sort_values("date_sk").reset_index(drop=True)

    # 5. Tabla de Hechos: fact_candidate_evaluations
    # Cruzamos con las dimensiones para obtener las Surrogate Keys
    fact = df.merge(
        dim_candidate,
        left_on=["First Name", "Last Name", "Email"],
        right_on=["first_name", "last_name", "email"],
    )
    fact = fact.merge(
        dim_technology,
        left_on=["Technology", "Seniority"],
        right_on=["technology_name", "seniority"],
    )
    fact = fact.merge(dim_location, left_on="Country", right_on="country")

    fact["application_date_sk"] = (
        fact["Application Date"].dt.strftime("%Y%m%d").astype(int)
    )
    fact["evaluation_id"] = fact.index + 1

    # Selección final de columnas de hechos y métricas
    fact_table = fact[
        [
            "evaluation_id",
            "candidate_sk",
            "technology_sk",
            "location_sk",
            "application_date_sk",
            "YOE",
            "Code Challenge Score",
            "Technical Interview Score",
            "is_hired",
        ]
    ].rename(
        columns={
            "YOE": "years_of_experience",
            "Code Challenge Score": "code_challenge_score",
            "Technical Interview Score": "technical_interview_score",
        }
    )

    print("Star Schema tables generated successfully:")
    print(f" - dim_candidate: {len(dim_candidate)} rows")
    print(f" - dim_technology: {len(dim_technology)} rows")
    print(f" - dim_location: {len(dim_location)} rows")
    print(f" - dim_date: {len(dim_date)} rows")
    print(f" - fact_candidate_evaluations: {len(fact_table)} rows")

    return {
        "dim_candidate": dim_candidate,
        "dim_technology": dim_technology,
        "dim_location": dim_location,
        "dim_date": dim_date,
        "fact_candidate_evaluations": fact_table,
    }


if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data

    # Prueba local de la construcción del modelo
    raw_data = extract_data("data/raw/candidates.csv")
    clean_data = transform_data(raw_data)
    tables = build_dimensional_model(clean_data)

    print("\nPreview of fact_candidate_evaluations:")
    print(tables["fact_candidate_evaluations"].head(3))