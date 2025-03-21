#!/usr/bin/env python3
"""
Bronze Layer SQL View Generator CLI

A tool to help create SQL views for BigQuery bronze layer transformations.
"""
import argparse
from src.bigquery_connector import BigQueryConnector
from src.template_manager import TemplateManager
from src.config_manager import ConfigManager
from src.sql_generator import SQLGenerator
from src.cli_manager import CLIManager

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Bronze Layer SQL View Generator CLI')
    
    parser.add_argument(
        '--credentials', 
        '-c',
        help='Path to the Google Cloud service account JSON credentials file'
    )
    
    return parser.parse_args()

def main():
    """Main entry point"""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Initialize components
    bq = BigQueryConnector(credentials_path=args.credentials)
    templates = TemplateManager()
    configs = ConfigManager()
    sql_generator = SQLGenerator(templates)
    
    # Run CLI Manager
    cli_manager = CLIManager(bq, templates, configs, sql_generator)
    cli_manager.run()

if __name__ == "__main__":
    main() 