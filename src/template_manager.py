"""
Module for managing SQL templates for different column types
"""
import os

class TemplateManager:
    """Manages SQL templates for different column types"""
    
    def __init__(self, template_dir="templates"):
        self.template_dir = template_dir
        self.templates = {}
        self.load_templates()
    
    def load_templates(self):
        """Load all SQL templates from the template directory"""
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Create default templates if they don't exist
        default_templates = {
            "base.sql": """-- Create the bronze dataset if it doesn't exist
CREATE SCHEMA IF NOT EXISTS `{bronze_dataset}`
OPTIONS (
  location = 'US'
);

-- Create or replace the view
CREATE OR REPLACE VIEW `{bronze_dataset}.{table_name}` AS
SELECT
{columns}
FROM `{source_dataset}.{table_name}`""",
            "string.sql": "CAST({column_name} AS STRING) AS {column_name}",
            "int.sql": "CAST({column_name} AS INT64) AS {column_name}",
            "float.sql": "CAST({column_name} AS FLOAT64) AS {column_name}",
            "timestamp.sql": "TIMESTAMP({column_name}) AS {column_name}",
            "date.sql": "DATE({column_name}) AS {column_name}"
        }
        
        for name, content in default_templates.items():
            filepath = os.path.join(self.template_dir, name)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write(content)
        
        # Load all templates
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.sql'):
                with open(os.path.join(self.template_dir, filename), 'r') as f:
                    template_name = filename.replace('.sql', '')
                    self.templates[template_name] = f.read()
    
    def get_template(self, template_name):
        """Get a specific template by name"""
        return self.templates.get(template_name)
    
    def get_available_templates(self):
        """Get list of available templates (excluding base)"""
        return [t for t in self.templates.keys() if t != 'base'] 