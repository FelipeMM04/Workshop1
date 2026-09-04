-- Create Database
CREATE DATABASE IF NOT EXISTS kimball_dw;
USE kimball_dw;

-- Dimension 1: dim_date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL
);

-- Dimension 2: dim_technology
CREATE TABLE IF NOT EXISTS dim_technology (
    technology_key INT AUTO_INCREMENT PRIMARY KEY,
    technology_name VARCHAR(100) NOT NULL,
    seniority VARCHAR(50) NOT NULL
);

-- Dimension 3: dim_candidate
CREATE TABLE IF NOT EXISTS dim_candidate (
    candidate_key INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    location VARCHAR(150)
);

-- Fact Table: fact_candidate_evaluations
CREATE TABLE IF NOT EXISTS fact_candidate_evaluations (
    evaluation_id INT PRIMARY KEY,
    date_key INT NOT NULL,
    technology_key INT NOT NULL,
    candidate_key INT NOT NULL,
    score FLOAT NOT NULL,
    is_hired INT NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (technology_key) REFERENCES dim_technology(technology_key),
    FOREIGN KEY (candidate_key) REFERENCES dim_candidate(candidate_key)
);