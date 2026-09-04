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

## 9. Star Schema Diagram

```mermaid
erDiagram
    dim_date {
        int date_key PK
        int year
        int month
        int day
        int quarter
    }

    dim_technology {
        int technology_key PK
        string technology_name
        string seniority
    }

    dim_candidate {
        int candidate_key PK
        int candidate_id
        string location
    }

    fact_candidate_evaluations {
        int evaluation_id PK
        int date_key FK
        int technology_key FK
        int candidate_key FK
        float score
        int is_hired
    }

    dim_date ||--o{ fact_candidate_evaluations : "1 : N"
    dim_technology ||--o{ fact_candidate_evaluations : "1 : N"
    dim_candidate ||--o{ fact_candidate_evaluations : "1 : N"

    ---

## 10. Explanation of Dimensions and Facts

### Fact Table
* **`fact_candidate_evaluations`**: Stores numerical measures (`score`, `is_hired`) and foreign keys referencing surrogate keys in the dimension tables.

### Dimension Tables
* **`dim_date`**: Contains time attributes (`year`, `month`, `day`, `quarter`) extracted from evaluation dates to allow temporal rollups.
* **`dim_technology`**: Holds technical stack metadata (`technology_name`, `seniority`).
* **`dim_candidate`**: Stores candidate demographic and location attributes.

---

## 11. ETL Architecture
The ETL process follows a Python/SQL pipeline:
1. **Extract:** Reads raw candidate evaluation records from CSV source files.
2. **Transform:** Cleans data, normalizes text columns, generates surrogate keys, and derives date dimensions.
3. **Load:** Populates dimension tables first and then loads facts into the `kimball_dw` database in MySQL.

---

## 12. Main Transformation Decisions
* **Surrogate Key Generation:** Created integer surrogate keys (`date_key`, `technology_key`, `candidate_key`) to decouple the DW from operational IDs.
* **Data Type Enforcement:** Converted evaluation scores and hiring indicators to uniform numerical types.
* **Null Handling:** Assigned default values (e.g., `'Unknown'`) for missing dimensional attributes.

---

## 13. Technologies
* **Database:** MySQL Server
* **ETL Engine:** Python (Pandas, SQLAlchemy) / SQL
* **BI & Data Visualization:** Microsoft Power BI
* **Version Control:** Git & GitHub

---

## 14. Instructions to Run the Project

### Prerequisites
* MySQL Server running locally or remotely.
* Python 3.x installed with required packages (`pandas`, `sqlalchemy`, `pymysql`).
* Power BI Desktop.

### Step-by-Step Execution
1. **Clone the Repository:**
   ```bash
   git clone <REPOSITORY_URL>
   cd <REPOSITORY_FOLDER>

   Setup Database:
Execute the DDL script in MySQL to create the kimball_dw schema and tables.

Execute ETL Script:

python etl_pipeline.py

Open Power BI Report:

Open the .pbix project file in Power BI Desktop.

Update the MySQL database connection credentials if prompted.

Refresh data to update visualizations.


Analytical Queries and KPIs

-- KPI 1: Annual Hires (R1)
SELECT d.year, SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year ASC;

-- KPI 2: Hires by Technology (R2)
SELECT t.technology_name, SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hires DESC;

-- KPI 3: Hires by Seniority (R4)
SELECT t.seniority, SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.seniority
ORDER BY total_hires DESC;

Main Business Findings
Temporal Trend: Candidate hiring grew steadily between 2018 and 2021 before experiencing a noticeable decrease in 2022.

Demand Leader: DevOps and Game Development roles represent the highest volume of successful hires across all evaluated technologies.

Seniority Distribution: Hires are well-distributed across seniority levels, with strong representation in mid-level and senior roles.

Final Requirements Validation
Requirements Validation Matrix

| Requirement | Implemented? | DW Tables Used | Query / KPI | Main Finding |
| :--- | :---: | :--- | :--- | :--- |
| **R1** | **Yes** | `fact_candidate_evaluations`, `dim_date` | `SUM(is_hired)` aggregated by year | Hiring volume grew steadily from 2018 to 2021 before dropping in 2022. |
| **R2** | **Yes** | `fact_candidate_evaluations`, `dim_technology` | `SUM(is_hired)` grouped by technology_name | DevOps and Game Development register the highest total volume of hires. |
| **R3** | **Yes** | `fact_candidate_evaluations`, `dim_candidate` | `COUNT(evaluation_id)` / `AVG(score)` by location | Evaluation volumes and average scores vary across geographic regions. |
| **R4** | **Yes** | `fact_candidate_evaluations`, `dim_technology` | `SUM(is_hired)` grouped by seniority | Hires are well-distributed across experience levels (mid-to-senior profiles lead). |
| **R5** | **Yes** | `fact_candidate_evaluations` | `AVG(score)` / `COUNT(is_hired = 1)` | Higher evaluation scores directly correlate with successful candidate hiring outcomes. |

Analytical Evaluation Questions
Does the final Data Warehouse provide enough information to satisfy all five business requirements?
Yes. The Kimball dimensional model (kimball_dw), through its central fact table and dimension tables, stores all candidate evaluation attributes and success metrics necessary to answer all analytical requirements (R1–R5).

Does the dimensional model contain elements that are not justified by the analytical requirements?
No. Every attribute and measure in the schema directly supports at least one defined KPI or business requirement, adhering to clean star schema design principles.

What business decisions can now be supported by the implemented analytical system?

Recruitment Sourcing: HR leadership can focus recruitment budgets on high-demand stacks like DevOps and Game Development.

Capacity Planning: Historical temporal trends enable HR to anticipate annual hiring cycles and adjust interviewing capacity.

Seniority Balancing: Profiling hires by experience level allows engineering management to balance team composition and control labor costs.