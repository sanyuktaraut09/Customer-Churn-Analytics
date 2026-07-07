-- SQL analysis for IBM Telco Customer Churn dataset
-- Assumes the dataset has been loaded into a table named customer_churn.
-- The table should contain columns such as customerID, gender, SeniorCitizen, Partner,
-- Dependents, tenure, Contract, PaymentMethod, InternetService, MonthlyCharges,
-- TotalCharges, and Churn.

-- 1. Total number of customers in the dataset.
SELECT COUNT(*) AS total_customers
FROM customer_churn;

-- 2. Overall churn rate as a percentage of total customers.
SELECT
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn;

-- 3. Overall retention rate as a percentage of total customers.
SELECT
    ROUND(SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS retention_rate_percent
FROM customer_churn;

-- 4. Number of customers by gender.
SELECT
    gender,
    COUNT(*) AS customer_count
FROM customer_churn
GROUP BY gender
ORDER BY customer_count DESC;

-- 5. Number of customers by contract type.
SELECT
    Contract AS contract_type,
    COUNT(*) AS customer_count
FROM customer_churn
GROUP BY Contract
ORDER BY customer_count DESC;

-- 6. Churn count and churn rate by contract type.
SELECT
    Contract AS contract_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_percent DESC;

-- 7. Churn count and churn rate by payment method.
SELECT
    PaymentMethod AS payment_method,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_percent DESC;

-- 8. Churn count and churn rate by internet service.
SELECT
    InternetService AS internet_service,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY InternetService
ORDER BY churn_rate_percent DESC;

-- 9. Average monthly charges by churn status.
SELECT
    Churn,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM customer_churn
GROUP BY Churn;

-- 10. Average tenure by churn status.
SELECT
    Churn,
    ROUND(AVG(tenure), 2) AS avg_tenure_months
FROM customer_churn
GROUP BY Churn;

-- 11. Total monthly revenue by contract type.
SELECT
    Contract AS contract_type,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue
FROM customer_churn
GROUP BY Contract
ORDER BY total_monthly_revenue DESC;

-- 12. Total monthly revenue by internet service.
SELECT
    InternetService AS internet_service,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue
FROM customer_churn
GROUP BY InternetService
ORDER BY total_monthly_revenue DESC;

-- 13. Top 10 highest paying customers by total charges.
SELECT
    customerID,
    gender,
    Contract,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges,
    Churn
FROM customer_churn
ORDER BY TotalCharges DESC
LIMIT 10;

-- 14. Senior citizen churn analysis: count and churn rate.
SELECT
    SeniorCitizen,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY SeniorCitizen
ORDER BY SeniorCitizen DESC;

-- 15. Partner status versus churn.
SELECT
    Partner,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY Partner
ORDER BY churn_rate_percent DESC;

-- 16. Dependents status versus churn.
SELECT
    Dependents,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY Dependents
ORDER BY churn_rate_percent DESC;

-- 17. Customers with tenure greater than 24 months.
SELECT
    customerID,
    gender,
    Contract,
    tenure,
    MonthlyCharges,
    TotalCharges,
    Churn
FROM customer_churn
WHERE tenure > 24
ORDER BY tenure DESC;

-- 18. Customers paying above average monthly charges.
WITH avg_monthly AS (
    SELECT AVG(MonthlyCharges) AS average_monthly_charges
    FROM customer_churn
)
SELECT
    cc.customerID,
    cc.gender,
    cc.Contract,
    cc.MonthlyCharges,
    cc.TotalCharges,
    cc.Churn
FROM customer_churn cc
JOIN avg_monthly am ON cc.MonthlyCharges > am.average_monthly_charges
ORDER BY cc.MonthlyCharges DESC;

-- 19. Estimated monthly revenue lost due to churn.
SELECT
    ROUND(SUM(MonthlyCharges) FILTER (WHERE Churn = 'Yes'), 2) AS monthly_revenue_lost_due_to_churn
FROM customer_churn;

-- 20. Create a summary view for dashboard reporting.
CREATE OR REPLACE VIEW customer_summary AS
SELECT
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    Contract,
    PaymentMethod,
    InternetService,
    MonthlyCharges,
    TotalCharges,
    Churn,
    CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END AS churn_flag,
    CASE WHEN Churn = 'No' THEN 1 ELSE 0 END AS retention_flag,
    CASE WHEN tenure > 24 THEN 1 ELSE 0 END AS long_tenure_flag,
    CASE WHEN MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customer_churn) THEN 1 ELSE 0 END AS above_average_monthly_flag
FROM customer_churn;

-- Additional query 21. Churn rate by gender.
SELECT
    gender,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM customer_churn
GROUP BY gender
ORDER BY churn_rate_percent DESC;

-- Additional query 22. Average tenure by contract type.
SELECT
    Contract AS contract_type,
    ROUND(AVG(tenure), 2) AS avg_tenure_months
FROM customer_churn
GROUP BY Contract
ORDER BY avg_tenure_months DESC;

-- Additional query 23. Average total charges by churn status.
SELECT
    Churn,
    ROUND(AVG(TotalCharges), 2) AS avg_total_charges
FROM customer_churn
GROUP BY Churn;

-- Additional query 24. Revenue lost due to churn by contract type.
SELECT
    Contract AS contract_type,
    ROUND(SUM(MonthlyCharges) FILTER (WHERE Churn = 'Yes'), 2) AS monthly_revenue_lost_due_to_churn
FROM customer_churn
GROUP BY Contract
ORDER BY monthly_revenue_lost_due_to_churn DESC;

-- Additional query 25. Top 10 customers by monthly charges and churn status.
SELECT
    customerID,
    gender,
    Contract,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges,
    Churn
FROM customer_churn
ORDER BY MonthlyCharges DESC
LIMIT 10;
