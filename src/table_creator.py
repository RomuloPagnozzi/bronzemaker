"""
Module for creating tables from SQL view files
"""
import os
import re

class TableCreator:
    """Creates BigQuery views from generated SQL files"""
    
    def __init__(self, bq_connector, datasets_dir="datasets"):
        """
        Initialize table creator.
        
        Args:
            bq_connector: BigQuery connector instance
            datasets_dir: Directory containing generated SQL files
        """
        self.bq = bq_connector
        self.datasets_dir = datasets_dir
    
    def list_available_datasets(self):
        """List all datasets with SQL files in the datasets directory"""
        if not os.path.exists(self.datasets_dir):
            return []
        
        return [d for d in os.listdir(self.datasets_dir) 
                if os.path.isdir(os.path.join(self.datasets_dir, d))]
    
    def list_available_tables(self, dataset_id):
        """List all tables with SQL files for a dataset"""
        dataset_dir = os.path.join(self.datasets_dir, dataset_id)
        if not os.path.exists(dataset_dir):
            return []
        
        return [f[:-4] for f in os.listdir(dataset_dir) if f.endswith('.sql')]
    
    def read_sql_file(self, dataset_id, table_id):
        """Read SQL file content"""
        sql_path = os.path.join(self.datasets_dir, dataset_id, f"{table_id}.sql")
        
        if not os.path.exists(sql_path):
            return None
        
        with open(sql_path, 'r') as f:
            return f.read()
    
    def extract_view_name(self, sql):
        """Extract the full view name from the SQL"""
        # Look for CREATE OR REPLACE VIEW `dataset.table` pattern
        pattern = r"CREATE OR REPLACE VIEW\s+`([^`]+)`"
        match = re.search(pattern, sql)
        if match:
            return match.group(1)
        return None
    
    def create_table(self, dataset_id, table_id):
        """Create a table from the SQL file"""
        # Read SQL query
        sql = self.read_sql_file(dataset_id, table_id)
        if not sql:
            return False, f"SQL file for {dataset_id}.{table_id} not found"
        
        # Execute query
        success, message = self.bq.execute_query(sql)
        
        if success:
            try:
                # Extract the full table name from the SQL
                view_name = self.extract_view_name(sql)
                
                if not view_name:
                    return True, {
                        "message": message,
                        "error": "Could not extract view name from SQL"
                    }
                
                # Preview the table
                preview_success, preview_data = self.bq.preview_table(f"`{view_name}`")
                
                if preview_success:
                    return True, {
                        "message": message,
                        "view_name": view_name,
                        "preview": preview_data
                    }
                else:
                    return True, {
                        "message": message,
                        "view_name": view_name,
                        "preview_error": preview_data
                    }
            except Exception as e:
                return True, {
                    "message": message,
                    "error": f"Could not preview table: {e}"
                }
        
        return success, message 