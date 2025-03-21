"""
Module for managing the main CLI interface
"""
import json
from src.interactive_cli import InteractiveCLI
from src.table_creator import TableCreator
from src.formatter import calculate_max_width, format_column_with_type, format_preview_row

class CLIManager:
    """Manages the main CLI interface with different operation modes"""
    
    def __init__(self, bq_connector, template_manager, config_manager, sql_generator):
        self.bq_connector = bq_connector
        self.template_manager = template_manager
        self.config_manager = config_manager
        self.sql_generator = sql_generator
        
        # Initialize sub-components
        self.interactive_cli = InteractiveCLI(
            bq_connector, template_manager, config_manager, sql_generator
        )
        self.table_creator = TableCreator(bq_connector)
    
    def select_operation_mode(self):
        """Let user select between generate SQL or create tables mode"""
        print("=== Bronze Layer SQL View Generator ===\n")
        print("Select operation mode:")
        print("1. Generate SQL views")
        print("2. Create tables from SQL files")
        
        while True:
            try:
                selection = input("\nEnter choice (number): ")
                mode = int(selection)
                if mode in [1, 2]:
                    return mode
                else:
                    print("Invalid selection. Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number (1 or 2).")
    
    def display_table_preview(self, preview_data):
        """Display table preview in a transposed format for better readability"""
        print(f"\nPreview of the table ({preview_data['row_count']} rows, {preview_data['column_count']} columns):")
        
        # Calculate the maximum width for alignment
        max_width = calculate_max_width(preview_data['schema'], preview_data['column_types'])
        
        # Display column types first
        print("\nColumn Types:")
        for col in preview_data['schema']:
            col_type = preview_data['column_types'][col]
            # Format the column name with right alignment
            formatted_col = format_column_with_type(col, col_type, max_width)
            print(f"{formatted_col}: {col_type}")
        
        # For each row, display a header with the row number
        for row_idx, row in enumerate(preview_data['rows'], 1):
            print(f"\n--- Row {row_idx} ---")
            
            # Format and display each column
            formatted_lines = format_preview_row(row, preview_data['schema'], 
                                               preview_data['column_types'], max_width)
            for line in formatted_lines:
                print(line)
    
    def display_table_preview_as_json(self, preview_data):
        """Display table preview in JSON format"""
        print(f"\nPreview of the table ({preview_data['row_count']} rows, {preview_data['column_count']} columns):")
        
        # Calculate the maximum width for alignment
        max_width = calculate_max_width(preview_data['schema'], preview_data['column_types'])
        
        # Display column types first
        print("\nColumn Types:")
        for col in preview_data['schema']:
            col_type = preview_data['column_types'][col]
            # Format the column name with right alignment
            formatted_col = format_column_with_type(col, col_type, max_width)
            print(f"{formatted_col}: {col_type}")
        
        print("\nData (JSON format):")
        print(json.dumps(preview_data['rows'], indent=2))
    
    def run_create_tables_mode(self):
        """Run the create tables mode"""
        print("\n=== Create Tables from SQL Files ===\n")
        
        # List available datasets
        datasets = self.table_creator.list_available_datasets()
        if not datasets:
            print("No datasets found with SQL files.")
            return
        
        print("Available datasets:")
        for i, dataset in enumerate(datasets, 1):
            print(f"{i}. {dataset}")
        
        # Select dataset
        while True:
            try:
                selection = input("\nSelect dataset (number): ")
                idx = int(selection) - 1
                if 0 <= idx < len(datasets):
                    dataset_id = datasets[idx]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # List available tables
        tables = self.table_creator.list_available_tables(dataset_id)
        if not tables:
            print(f"No SQL files found for dataset: {dataset_id}")
            return
        
        print(f"\nTables available in {dataset_id}:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        
        # Select table
        while True:
            try:
                selection = input("\nSelect table to create (number): ")
                idx = int(selection) - 1
                if 0 <= idx < len(tables):
                    table_id = tables[idx]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Create bronze view
        print(f"\nCreating bronze view for table: {dataset_id}.{table_id}...")
        success, result = self.table_creator.create_table(dataset_id, table_id)
        
        if success:
            if isinstance(result, dict):
                print(f"\nSuccess: {result['message']}")
                print(f"View created: {result['view_name']}")
                
                if "preview" in result:
                    # Display preview with the new format
                    print("\nHow would you like to view the preview?")
                    print("1. Transposed (column: value format)")
                    print("2. JSON format")
                    
                    while True:
                        try:
                            view_mode = int(input("\nEnter choice (number): "))
                            if view_mode == 1:
                                self.display_table_preview(result["preview"])
                                break
                            elif view_mode == 2:
                                self.display_table_preview_as_json(result["preview"])
                                break
                            else:
                                print("Invalid selection. Please enter 1 or 2.")
                        except ValueError:
                            print("Please enter a valid number.")
                            
                elif "preview_error" in result:
                    print(f"\nError previewing table: {result['preview_error']}")
                elif "error" in result:
                    print(f"\nError: {result['error']}")
            else:
                print(f"\nSuccess: {result}")
        else:
            print(f"\nError: {result}")
    
    def run(self):
        """Main entry point for the CLI"""
        mode = self.select_operation_mode()
        
        if mode == 1:
            # Generate SQL views mode
            self.interactive_cli.run()
        elif mode == 2:
            # Create tables mode
            self.run_create_tables_mode() 