WITH RECURSIVE date_series AS (
    SELECT DATE(MIN(transaction_date)) AS date
    FROM transactions
    UNION ALL
    SELECT DATE(date, '+1 day')
    FROM date_series
    WHERE DATE(date, '+1 day') <= (
            SELECT DATE(MAX(transaction_date))
            FROM transactions
        )
),
active_accounts AS (
    SELECT ds.date AS report_date,
        t.account_id
    FROM date_series ds
        JOIN transactions t ON DATE(t.transaction_date) BETWEEN DATE(ds.date, '-44 days') AND ds.date
    WHERE t.transaction_type = 'transfer'
        AND t.transaction_date IS NOT NULL
    GROUP BY ds.date,
        t.account_id
    HAVING COUNT(DISTINCT t.transaction_id) >= 2
)
SELECT strftime('%Y-%m', report_date) AS month,
    COUNT(DISTINCT account_id) AS active_account_count
FROM active_accounts
GROUP BY strftime('%Y-%m', report_date)
ORDER BY month;