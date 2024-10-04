WITH RECURSIVE date_series AS (
    SELECT DATE(MIN(transaction_date)) AS date
    FROM transaction_tab
    UNION ALL
    SELECT DATE(date, '+1 day')
    FROM date_series
    WHERE DATE(date, '+1 day') <= (
            SELECT DATE(MAX(transaction_date))
            FROM transaction_tab
        )
),
active_accounts AS (
    SELECT ds.date AS report_date,
        t.account_id
    FROM date_series ds
        JOIN transaction_tab t ON DATE(t.transaction_date) BETWEEN DATE(ds.date, '-44 days') AND ds.date
    WHERE json_extract(t.payload, '$.transaction_type') = 'transfer'
        AND json_extract(t.payload, '$.status') = 'success'
    GROUP BY ds.date,
        t.account_id
    HAVING COUNT(DISTINCT t.transaction_id) >= 2
)
SELECT strftime('%Y-%m', report_date) AS month,
    COUNT(DISTINCT account_id) AS active_account_count
FROM active_accounts
GROUP BY strftime('%Y-%m', report_date)
ORDER BY month;