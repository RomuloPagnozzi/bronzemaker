CASE WHEN TRIM({column_name}) = '' THEN NULL ELSE CAST(TRIM({column_name}) AS INT64) END AS {column_name}