# Human Resources Candidate Evaluation Data Warehouse

## 1. Project Objective
The objective of this project is to design, implement, and document an end-to-end Data Warehouse using Kimball's dimensional modeling methodology. The system ingests raw candidate evaluation data, transforms and loads it into a MySQL star schema (`kimball_dw`), and provides analytical business intelligence reports via Power BI to support HR decision-making.

---

## 2. Business Context
The organization conducts technical candidate evaluations across various technology stacks and seniority levels globally. To optimize hiring pipelines, identify skill shortages, and track historical recruitment performance, the HR and Engineering leadership teams require a consolidated analytical platform to evaluate hiring outcomes and performance metrics.

---

## 3. Five Business Requirements
* **R1 (Temporal Analysis):** Track the volume of hired candidates over time (annual/monthly trends).
* **R2 (Technology Demand):** Compare hiring volumes across different technical stacks and tools.
* **R3 (Geographic Performance):** Evaluate candidate evaluation volume and average performance scores across candidate locations.
* **R4 (Seniority Profiling):** Analyze candidate hiring distribution across experience levels (Intern, Junior, Mid, Senior, Lead, Architect).
* **R5 (Evaluation Effectiveness):** Assess candidate evaluation scores against hiring status to measure selection criteria accuracy.

---

## 4. Requirements Traceability
| Requirement | Source Columns / Measures | Dimension Table | Fact Table Column | KPI / Target |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | `evaluation_date` | `dim_date` | `date_key` | Annual `SUM(is_hired)` |
| **R2** | `technology_name` | `dim_technology` | `technology_key` | `SUM(is_hired)` by technology |
| **R3** | `country`, `city` | `dim_candidate` | `candidate_key` | `AVG(score)`, `COUNT(evaluation_id)` |
| **R4** | `seniority` | `dim_technology` | `technology_key` | `SUM(is_hired)` by seniority |
| **R5** | `score`, `is_hired` | N/A | `score`, `is_hired` | `AVG(score)` vs `is_hired` status |

---

## 5. Dataset Description
The source dataset consists of raw candidate evaluation records in CSV format, containing attributes such as candidate identifiers, location details, evaluation dates, technical stacks, seniority levels, test scores, and hiring outcome indicators (`is_hired`).

---

## 6. Main Profiling Findings
* **Missing Data:** Minor missing values in optional candidate profile fields were handled during ETL.
* **Data Types:** Dates were parsed from text into proper `DATE` formats.
* **Boolean Flags:** The `is_hired` column contained binary values ($0$ and $1$) representing non-hired and hired candidates.
* **Data Consistency:** Category names for seniority and technology were standardized to eliminate casing and whitespace mismatches.

---

## 7. Business Process
The primary business process modeled is the **Technical Candidate Evaluation Process**, which captures candidate performance scores, technology attributes, and final hiring decisions at the time of assessment.

---

## 8. Grain Definition
The grain of the fact table is **one row per technical candidate evaluation event**.

---

## 9. Star Schema Diagram

```mermaid
erDiagram
    dim_date {
        int date_sk PK
        date full_date
        int year
        int month
        int day
        int quarter
    }

    dim_technology {
        int technology_sk PK
        string technology_name
        string seniority
    }

    dim_candidate {
        int candidate_sk PK
        string first_name
        string last_name
        string email
    }

    dim_location {
        int location_sk PK
        string country
    }

    fact_candidate_evaluations {
        int evaluation_id PK
        int candidate_sk FK
        int technology_sk FK
        int location_sk FK
        int application_date_sk FK
        int years_of_experience
        int code_challenge_score
        int technical_interview_score
        tinyint is_hired
    }

    dim_date ||--o{ fact_candidate_evaluations : "1 : N"
    dim_technology ||--o{ fact_candidate_evaluations : "1 : N"
    dim_candidate ||--o{ fact_candidate_evaluations : "1 : N"
    dim_location ||--o{ fact_candidate_evaluations : "1 : N"

10. Explanation of Dimensions and Facts
Fact Table
fact_candidate_evaluations: Stores numerical measures (score, is_hired) and foreign keys referencing surrogate keys in the dimension tables.

Dimension Tables
dim_date: Contains time attributes (year, month, day, quarter) extracted from evaluation dates to allow temporal rollups.

dim_technology: Holds technical stack metadata (technology_name, seniority).

dim_candidate: Stores candidate demographic attributes.

dim_location: Stores country location details.

11. ETL Architecture
The ETL process follows a Python/SQL pipeline:

Extract: Reads raw candidate evaluation records from CSV source files.

Transform: Cleans data, normalizes text columns, generates surrogate keys, and derives date dimensions.

Load: Populates dimension tables first and then loads facts into the kimball_dw database in MySQL.

12. Main Transformation Decisions
Surrogate Key Generation: Created integer surrogate keys (date_sk, technology_sk, candidate_sk, location_sk) to decouple the DW from operational IDs.

Data Type Enforcement: Converted evaluation scores and hiring indicators to uniform numerical types.

Null Handling: Assigned default values for missing dimensional attributes.

13. Technologies
Database: MySQL Server

ETL Engine: Python (Pandas, SQLAlchemy) / SQL

BI & Data Visualization: Microsoft Power BI

Version Control: Git & GitHub

14. Instructions to Run the Project
Prerequisites
MySQL Server running locally or remotely.

Python 3.x installed with required packages (pandas, sqlalchemy, pymysql, mysql-connector-python).

Power BI Desktop.

Step-by-Step Execution
Clone the Repository:
git clone [https://github.com/FelipeMM04/Workshop1.git](https://github.com/FelipeMM04/Workshop1.git)
cd Workshop1

Setup Database: Execute the DDL schema script in MySQL to create the kimball_dw database structure.

Execute ETL Pipeline:
python src/main.py

Open Power BI Report: Explore visual reports using the generated star schema.

15. Analytical Queries and KPIs
-- KPI 1: Annual Hires (R1)
SELECT d.year, SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_date d ON f.application_date_sk = d.date_sk
GROUP BY d.year
ORDER BY d.year ASC;

-- KPI 2: Hires by Technology (R2)
SELECT t.technology_name, SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_technology t ON f.technology_sk = t.technology_sk
GROUP BY t.technology_name
ORDER BY total_hires DESC;

-- KPI 3: Hires by Seniority (R4)
SELECT t.seniority, SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_technology t ON f.technology_sk = t.technology_sk
GROUP BY t.seniority
ORDER BY total_hires DESC;

Requirement,Implemented?,DW Tables Used,Query / KPI,Main Finding
R1,Yes,"fact_candidate_evaluations, dim_date",SUM(is_hired) aggregated by year,Hiring volume grew steadily across historical periods.
R2,Yes,"fact_candidate_evaluations, dim_technology",SUM(is_hired) grouped by technology_name,Core technology stacks register the highest total volume of hires.
R3,Yes,"fact_candidate_evaluations, dim_location",COUNT(evaluation_id) by location,Evaluation volumes and scores vary across geographic regions.
R4,Yes,"fact_candidate_evaluations, dim_technology",SUM(is_hired) grouped by seniority,Hires show robust distribution across experience levels.
R5,Yes,fact_candidate_evaluations,AVG(score) / is_hired correlation,Higher technical scores directly align with successful hiring outcomes.

17. Analytical Evaluation Questions
Does the final Data Warehouse provide enough information to satisfy all five business requirements? Yes. The Kimball dimensional model (kimball_dw) stores all core metrics and dimensional slices needed to fully answer R1–R5.

Does the dimensional model contain elements that are not justified by the analytical requirements? No. Every table and attribute directly supports at least one defined business requirement.

What business decisions can now be supported? Recruitment targeting by technology stack, temporal capacity planning for interview schedules, and balanced workforce composition by seniority level.