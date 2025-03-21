-- Create the bronze dataset if it doesn't exist
CREATE SCHEMA IF NOT EXISTS `{bronze_dataset}`
OPTIONS (
  location = 'US'
);

-- Create or replace the view
CREATE OR REPLACE VIEW `{bronze_dataset}.{table_name}` AS
SELECT
{columns}
FROM `{source_dataset}.{table_name}`