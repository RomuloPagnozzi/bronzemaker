# Bronze Maker

A command-line tool that generates BigQuery SQL views for data ingestion (bronze layer) through an interactive process.

## Installation

1. Clone this repository
2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Authentication

You have two options for authenticating with Google Cloud:

### Option 1: Using Application Default Credentials

If you have `gcloud` CLI installed, you can run:

```
gcloud auth application-default login
```

### Option 2: Using Service Account JSON

If you have a service account JSON credentials file:

1. Store the JSON file securely on your system
2. Run the tool with the `--credentials` option:

```
python main.py --credentials /path/to/your/credentials.json
```

## Usage

Run the tool using:

```
python main.py
```

### Operation Modes

The tool has two operation modes:

#### 1. Generate SQL Views

This mode lets you create SQL view definitions by:

1. Selecting a BigQuery dataset
2. Choosing a table
3. For each column, viewing information and selecting a transformation template
4. Saving the configuration to a JSON file
5. Generating the SQL view file

#### 2. Create Tables from SQL Files

This mode lets you execute the generated SQL files to create the actual views in BigQuery:

1. Select a dataset from your local files
2. Choose a SQL file to execute
3. The tool will:
   - Create the bronze dataset if it doesn't exist
   - Execute the SQL to create/replace the view in BigQuery
   - Run a preview query (SELECT * LIMIT 5) on the new view
   - Display the column types and data in one of two formats:
     - Transposed format (better for wide tables with many columns)
     - JSON format (shows raw data structure)

## Dataset Naming Convention

The tool handles dataset naming according to these rules:

- If the source dataset name ends with `_raw` (e.g., `mydata_raw`), the tool automatically creates views in a corresponding `_bronze` dataset (e.g., `mydata_bronze`)
- If the source dataset doesn't end with `_raw`, the tool appends `_bronze` to the dataset name (e.g., `mydata` → `mydata_bronze`)
- The generated SQL automatically includes a `CREATE SCHEMA IF NOT EXISTS` statement to ensure the bronze dataset exists

## Templates

Templates are stored in the `templates/` directory as SQL files:

- `base.sql`: The base template for the entire view
- `string.sql`, `int.sql`, etc.: Templates for specific column types
- `unix_timestamp.sql`: Template for Unix timestamps (seconds)
- `unix_timestamp_ms.sql`: Template for Unix timestamps (milliseconds)

You can edit these templates to customize the transformations or add new ones.

## Configuration

Configurations for each table are stored as JSON files in:

```
configs/{dataset_name}/{table_name}.json
```

These files map column names to template types.

## Project Structure

```
/
├── main.py             
├── requirements.txt    
├── src/                
│ ├── init.py
│ ├── bigquery_connector.py
│ ├── cli_manager.py          
│ ├── config_manager.py       
│ ├── formatter.py            
│ ├── interactive_cli.py      
│ ├── sql_generator.py        
│ ├── table_creator.py        
│ ├── template_manager.py     
│ └── utils/                  
│ └── regenerate.py           # Utility to regenerate SQL from configs
├── templates/                # SQL templates for transformations
│   ├── base.sql
│   ├── string.sql
│   └── ...
├── configs/                  # Intermediate JSON configs
│   └── {dataset_name}/
│       └── {table_name}.json
└── datasets/                 # Generated SQL view files
    └── {dataset_name}/
        └── {table_name}.sql
```

## Feature Highlights

- **Interactive schema analysis**: The tool guides you through each column in a table, showing sample values and statistics to help you choose the right transformations.
- **Customizable templates**: Add or edit templates for different transformation needs.
- **Table creation and preview**: Create tables directly from SQL files and preview the results. 
- **Formatted table previews**: Table previews with well-aligned column names and types for better readability.
  - Column names and types are right-aligned at the colon for easy scanning
  - Both transposed and JSON view options available
  - Column data types are displayed alongside values 