#!/usr/bin/env python3
"""
Utility to regenerate SQL views from existing configuration files
"""
import os
import json
import argparse
from src.template_manager import TemplateManager
from src.sql_generator import SQLGenerator

def regenerate_sql(dataset_id, table_id, config_dir="configs", output_dir="datasets"):
    """Regenerate SQL file from existing config file"""
    # Check if config file exists
    config_path = os.path.join(config_dir, dataset_id, f"{table_id}.json")
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return False
    
    # Load config
    with open(config_path, 'r') as f:
        column_configs = json.load(f)
    
    # Generate SQL
    template_manager = TemplateManager()
    sql_generator = SQLGenerator(template_manager, output_dir)
    sql_path = sql_generator.generate_sql(dataset_id, table_id, column_configs)
    
    print(f"SQL view file regenerated: {sql_path}")
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Regenerate SQL views from config files')
    parser.add_argument('dataset_id', help='Dataset ID')
    parser.add_argument('table_id', help='Table ID')
    
    args = parser.parse_args()
    regenerate_sql(args.dataset_id, args.table_id)

if __name__ == "__main__":
    main() 