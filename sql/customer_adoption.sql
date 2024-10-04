WITH first_transactions AS (
  SELECT account_id,
    strftime('%Y-%m', transaction_date) AS transaction_month,
    json_extract(payload, '$.transaction_type') AS transaction_type,
    ROW_NUMBER() OVER (
      PARTITION BY account_id,
      json_extract(payload, '$.transaction_type')
      ORDER BY transaction_date
    ) AS rn
  FROM transaction_tab
  WHERE json_extract(payload, '$.status') = 'success'
)
SELECT transaction_month,
  transaction_type,
  COUNT(DISTINCT account_id) AS new_adopters
FROM first_transactions
WHERE rn = 1
GROUP BY transaction_month,
  transaction_type
ORDER BY transaction_month,
  transaction_type;