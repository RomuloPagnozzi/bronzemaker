"""
Module for generating SQL views based on templates and configurations
"""
import os

class SQLGenerator:
    """Generates SQL views based on templates and configurations"""
    
    def __init__(self, template_manager, output_dir="datasets"):
        self.template_manager = template_manager
        self.output_dir = output_dir
    
    def generate_sql(self, dataset_id, table_id, column_configs):
        """Generate SQL view for a table based on column configurations"""
        base_template = self.template_manager.get_template('base')
        
        # Generate column transformations
        column_sql = []
        for column_name, template_type in column_configs.items():
            if template_type == 'skip':
                continue
            elif template_type == 'custom':
                column_sql.append(f"    -- custom: {column_name}")
            else:
                template = self.template_manager.get_template(template_type)
                if template:
                    column_sql.append(f"    {template.format(column_name=column_name)}")
        
        # Determine the source and bronze dataset names
        source_dataset = dataset_id
        if dataset_id.endswith("_raw"):
            bronze_dataset = dataset_id.replace("_raw", "_bronze")
        else:
            bronze_dataset = f"{dataset_id}_bronze"
        
        # Format the final SQL
        sql = base_template.format(
            source_dataset=source_dataset,
            bronze_dataset=bronze_dataset,
            table_name=table_id,
            columns=',\n'.join(column_sql)
        )
        
        # Write to file
        dataset_dir = os.path.join(self.output_dir, dataset_id)
        os.makedirs(dataset_dir, exist_ok=True)
        
        sql_path = os.path.join(dataset_dir, f"{table_id}.sql")
        with open(sql_path, 'w') as f:
            f.write(sql)
        
        return sql_path 