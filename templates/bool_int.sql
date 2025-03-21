CASE 
  WHEN TRIM({column_name}) = '' THEN NULL 
  WHEN TRIM({column_name}) = '0' THEN FALSE 
  ELSE TRUE 
END AS {column_name} 