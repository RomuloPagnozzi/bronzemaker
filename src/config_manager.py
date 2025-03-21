"""
Module for managing configuration files for table transformations
"""
import os
import json

class ConfigManager:
    """Manages configuration files for table transformations"""
    
    def __init__(self, config_dir="configs"):
        self.config_dir = config_dir
    
    def save_config(self, dataset_id, table_id, config):
        """Save table transformation config to JSON file"""
        dataset_dir = os.path.join(self.config_dir, dataset_id)
        os.makedirs(dataset_dir, exist_ok=True)
        
        config_path = os.path.join(dataset_dir, f"{table_id}.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_path
    
    def load_config(self, dataset_id, table_id):
        """Load table transformation config from JSON file"""
        config_path = os.path.join(self.config_dir, dataset_id, f"{table_id}.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return None 