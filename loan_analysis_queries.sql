SELECT COUNT(*) as total_rows FROM cleaned_loan_data;

SELECT city,
       MAX("loan_burden_%") AS max_loan_burden
FROM cleaned_loan_data
GROUP BY city
ORDER BY max_loan_burden DESC
LIMIT 10;

SELECT loan_purpose,
       MAX(loan_amount) AS max_loan_amount
FROM cleaned_loan_data
GROUP BY loan_purpose
ORDER BY max_loan_amount DESC
LIMIT 10;

SELECT risk_level,
       COUNT(*) AS total_borrowers
FROM cleaned_loan_data
GROUP BY risk_level
ORDER BY total_borrowers DESC;

SELECT social_class,
       COUNT(*) AS total_borrowers,
       MAX(loan_amount) AS max_loan_amount,
       AVG(loan_amount) AS avg_loan_amount
FROM cleaned_loan_data
GROUP BY social_class
ORDER BY avg_loan_amount DESC
LIMIT 10;

SELECT city,
       COUNT(*) AS high_risk_count
FROM cleaned_loan_data
WHERE risk_level = 'High Risk'
GROUP BY city;

SELECT type_of_house,
       COUNT(*) AS total_borrowers,
       AVG("loan_burden_%") AS avg_loan_burden,
       MAX("loan_burden_%") AS max_loan_burden
FROM cleaned_loan_data
GROUP BY type_of_house
ORDER BY avg_loan_burden DESC;

SELECT primary_business,
       COUNT(*) AS total_borrowers,
       MAX(loan_amount) AS max_loan
FROM cleaned_loan_data
GROUP BY primary_business
ORDER BY max_loan DESC
LIMIT 10;