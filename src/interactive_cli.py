from src.bigquery_connector import BigQueryConnector
from src.template_manager import TemplateManager
from src.config_manager import ConfigManager
from src.sql_generator import SQLGenerator

"""
Module for the interactive command-line interface
"""

class InteractiveCLI:
    """Interactive command-line interface for the tool"""
    
    def __init__(self, bq_connector, template_manager, config_manager, sql_generator):
        self.bq = bq_connector
        self.templates = template_manager
        self.configs = config_manager
        self.sql_generator = sql_generator
    
    def select_dataset(self):
        """Interactive dataset selection"""
        datasets = self.bq.list_datasets()
        
        print("\nAvailable datasets:")
        for i, dataset in enumerate(datasets, 1):
            print(f"{i}. {dataset}")
        
        while True:
            try:
                selection = input("Select dataset (number): ")
                idx = int(selection) - 1
                if 0 <= idx < len(datasets):
                    return datasets[idx]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_table(self, dataset_id):
        """Interactive table selection"""
        tables = self.bq.list_tables(dataset_id)
        
        print(f"\nTables in {dataset_id}:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        
        while True:
            try:
                selection = input("Select table (number): ")
                idx = int(selection) - 1
                if 0 <= idx < len(tables):
                    return tables[idx]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def show_column_details(self, dataset_id, table_id, column_name):
        """Show detailed information about a column"""
        print(f"\n--- Detailed information for column: {column_name} ---")
        
        # Get column statistics
        stats = self.bq.get_column_stats(dataset_id, table_id, column_name)
        if "error" in stats:
            print(f"Error getting stats: {stats['error']}")
        else:
            print(f"Total rows: {stats['total_count']}")
            print(f"Null values: {stats['null_count']} ({100-stats['not_null_percent']}%)")
            print(f"Empty strings: {stats['empty_string_count']}")
            print(f"Not null: {stats['not_null_percent']}%")
        
        # Get most common values
        unique_values = self.bq.get_unique_values(dataset_id, table_id, column_name)
        if unique_values:
            print("\nMost common values (value, count):")
            for value, count in unique_values:
                print(f"  - {value}: {count}")
        
        input("\nPress Enter to continue...")
    
    def process_columns(self, dataset_id, table_id):
        """Interactive column transformation selection"""
        schema = self.bq.get_table_schema(dataset_id, table_id)
        available_templates = self.templates.get_available_templates() + ['custom', 'skip']
        column_configs = {}
        
        for field in schema:
            while True:
                print(f"\nColumn: {field.name}")
                print(f"Type: {field.field_type}")
                
                # Get sample values
                samples = self.bq.get_sample_values(dataset_id, table_id, field.name)
                print("Sample values:")
                for sample in samples:
                    print(f"  - {sample}")
                
                # Print available templates
                print("\nSelect transformation template:")
                for i, template in enumerate(available_templates, 1):
                    print(f"{i}. {template}")
                print(f"{len(available_templates) + 1}. Get more details")
                
                # Get user selection
                try:
                    selection = input("Enter choice (number): ")
                    idx = int(selection) - 1
                    
                    if idx == len(available_templates):
                        # Show more details
                        self.show_column_details(dataset_id, table_id, field.name)
                        continue  # Go back to template selection
                    elif 0 <= idx < len(available_templates):
                        template_type = available_templates[idx]
                        column_configs[field.name] = template_type
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        
        # Save configuration
        config_path = self.configs.save_config(dataset_id, table_id, column_configs)
        print(f"Configuration saved to: {config_path}")
        return column_configs
    
    def run(self):
        """Main CLI flow"""
        print("\n=== Generate SQL Views ===\n")
        
        # Dataset and table selection
        dataset_id = self.select_dataset()
        table_id = self.select_table(dataset_id)
        
        # Process columns
        print(f"\nProcessing table: {dataset_id}.{table_id}")
        column_configs = self.process_columns(dataset_id, table_id)
        
        # Generate SQL
        sql_path = self.sql_generator.generate_sql(dataset_id, table_id, column_configs)
        print(f"\nSQL view file generated: {sql_path}") 