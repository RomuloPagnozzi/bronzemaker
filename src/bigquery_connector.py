"""
Module for handling BigQuery connections and queries
"""
import os
from google.cloud import bigquery
from google.oauth2 import service_account

class BigQueryConnector:
    """Handles BigQuery connections and queries"""
    
    def __init__(self, credentials_path=None):
        """
        Initialize BigQuery connector.
        
        Args:
            credentials_path (str, optional): Path to the service account JSON credentials file.
                If not provided, uses application default credentials.
        """
        if credentials_path and os.path.exists(credentials_path):
            # Use service account credentials file
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = bigquery.Client(credentials=credentials)
        else:
            # Use application default credentials
            self.client = bigquery.Client()
    
    def list_datasets(self):
        """List all available datasets"""
        return [dataset.dataset_id for dataset in self.client.list_datasets()]
    
    def list_tables(self, dataset_id):
        """List all tables in a dataset"""
        return [table.table_id for table in self.client.list_tables(dataset_id)]
    
    def get_table_schema(self, dataset_id, table_id):
        """Get schema information for a table"""
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        return table.schema
    
    def get_sample_values(self, dataset_id, table_id, column_name):
        """Get 3 random non-empty sample values from a column"""
        query = f"""
        SELECT {column_name}
        FROM `{self.client.project}.{dataset_id}.{table_id}`
        WHERE {column_name} IS NOT NULL 
        AND TRIM(CAST({column_name} AS STRING)) != ''
        ORDER BY RAND()
        LIMIT 3
        """
        try:
            results = self.client.query(query).result()
            return [str(row[0]) for row in results]
        except Exception as e:
            return [f"Error retrieving samples: {e}"]
    
    def get_unique_values(self, dataset_id, table_id, column_name):
        """Get up to 3 unique values from a column with counts"""
        query = f"""
        SELECT 
            {column_name},
            COUNT(*) as count
        FROM `{self.client.project}.{dataset_id}.{table_id}`
        WHERE {column_name} IS NOT NULL
        GROUP BY {column_name}
        ORDER BY count DESC
        LIMIT 3
        """
        try:
            results = self.client.query(query).result()
            return [(str(row[0]), row[1]) for row in results]
        except Exception as e:
            return [(f"Error retrieving unique values: {e}", 0)]
    
    def get_column_stats(self, dataset_id, table_id, column_name):
        """Get basic statistics for a column"""
        query = f"""
        SELECT 
            COUNT(*) as total_count,
            COUNTIF({column_name} IS NULL) as null_count,
            COUNTIF(CAST({column_name} AS STRING) = '') as empty_string_count
        FROM `{self.client.project}.{dataset_id}.{table_id}`
        """
        try:
            row = next(self.client.query(query).result())
            return {
                "total_count": row.total_count,
                "null_count": row.null_count,
                "empty_string_count": row.empty_string_count,
                "not_null_percent": round(100 * (row.total_count - row.null_count) / row.total_count, 2) if row.total_count > 0 else 0
            }
        except Exception as e:
            return {"error": str(e)}
    
    def execute_query(self, query):
        """Execute a SQL query"""
        try:
            job = self.client.query(query)
            job.result()  # Wait for the job to complete
            return True, f"Query executed successfully. Job ID: {job.job_id}"
        except Exception as e:
            return False, f"Error executing query: {e}"
    
    def preview_table(self, full_table_name, limit=5):
        """Execute a SELECT * LIMIT query on a table and return results in a structured format"""
        query = f"SELECT * FROM {full_table_name} LIMIT {limit}"
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Get schema information with column types
            schema_fields = query_job.result().schema
            
            # Create a list of column names
            column_names = [field.name for field in schema_fields]
            
            # Create a dictionary mapping column names to types
            column_types = {field.name: field.field_type for field in schema_fields}
            
            # Format results as a list of dictionaries (rows)
            rows = []
            for row in results:
                rows.append({col: str(val) for col, val in row.items()})
                
            return True, {
                "schema": column_names,
                "column_types": column_types,
                "rows": rows,
                "row_count": len(rows),
                "column_count": len(column_names)
            }
        except Exception as e:
            return False, f"Error previewing table: {e}" 