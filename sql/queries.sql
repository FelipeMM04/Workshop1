USE kimball_dw;

-- R1: Temporal Analysis (Hired candidates over time)
SELECT 
    d.year, 
    SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year ASC;

-- R2: Technology Demand (Hired candidates by technology stack)
SELECT 
    t.technology_name, 
    SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hires DESC;

-- R3: Geographic Performance (Candidate evaluation volume and average score by location)
SELECT 
    c.location, 
    COUNT(f.evaluation_id) AS total_evaluations,
    AVG(f.score) AS average_score
FROM fact_candidate_evaluations f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.location
ORDER BY total_evaluations DESC;

-- R4: Seniority Distribution (Hired candidates by experience level)
SELECT 
    t.seniority, 
    SUM(f.is_hired) AS total_hires
FROM fact_candidate_evaluations f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.seniority
ORDER BY total_hires DESC;

-- R5: Evaluation Score Effectiveness (Average score by hiring decision)
SELECT 
    f.is_hired, 
    COUNT(f.evaluation_id) AS total_candidates,
    AVG(f.score) AS average_score
FROM fact_candidate_evaluations f
GROUP BY f.is_hired;