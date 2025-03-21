"""
Formatter module for consistent display formatting
"""

def format_column_with_type(col_name, col_type, max_width):
    """
    Format a column name and type for aligned display.
    
    Args:
        col_name: The column name
        col_type: The column type
        max_width: Maximum width needed for alignment
        
    Returns:
        Formatted string with right-aligned column name + type
    """
    col_with_type = f"{col_name} ({col_type})"
    # Fixed: Ensure exact right-alignment by using a fixed width for all columns
    return col_with_type.rjust(max_width)

def calculate_max_width(schema, column_types):
    """
    Calculate the maximum width needed for column name + type.
    
    Args:
        schema: List of column names
        column_types: Dictionary mapping column names to types
        
    Returns:
        Maximum width needed for alignment
    """
    # Get the exact maximum width for consistent alignment
    return max(len(col) + len(column_types[col]) + 3 for col in schema)  # +3 for "( )"

def format_preview_row(row, schema, column_types, max_width=None):
    """
    Format a preview row with aligned columns.
    
    Args:
        row: Dictionary containing column values
        schema: List of column names
        column_types: Dictionary mapping column names to types
        max_width: Optional pre-calculated max width
        
    Returns:
        List of formatted lines for display
    """
    if max_width is None:
        max_width = calculate_max_width(schema, column_types)
    
    lines = []
    for col in schema:
        col_type = column_types[col]
        # Format column name and type
        formatted_col = format_column_with_type(col, col_type, max_width)
        
        # Limit value length for display
        value = row[col]
        if len(value) > 100:
            value = value[:97] + "..."
        
        # Create the display line with consistent spacing after colon
        lines.append(f"{formatted_col}: {value}")
    
    return lines 