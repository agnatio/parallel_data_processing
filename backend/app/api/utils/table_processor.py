"""
Utility module for generating and processing tabular data
"""
import io
import csv
import random
import string
import logging
from typing import List, Dict, Any, Union, Optional
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


logger = logging.getLogger("app")


class TableProcessor:
    """Utility class for generating and processing tabular data"""
    
    # Data type options for column generation
    DATA_TYPES = [
        "string", "integer", "float", "date", "boolean", 
        "email", "name", "address", "product", "price"
    ]
    
    # Sample column names by category
    COLUMN_NAMES = {
        "string": ["description", "comments", "category", "department", "status", "type"],
        "integer": ["id", "quantity", "count", "age", "code", "stock"],
        "float": ["amount", "percentage", "ratio", "value", "score"],
        "date": ["date", "created_at", "updated_at", "expiry_date", "birth_date"],
        "boolean": ["is_active", "is_valid", "is_completed", "approved", "in_stock"],
        "email": ["email", "contact_email", "support_email", "billing_email"],
        "name": ["full_name", "first_name", "last_name", "user_name", "contact_name"],
        "address": ["address", "street", "city", "state", "country", "zip_code"],
        "product": ["product_name", "sku", "model", "brand", "category"],
        "price": ["price", "cost", "retail_price", "discount", "tax"]
    }

    @classmethod
    def generate_table_data(
        cls, 
        num_rows: int = 10, 
        num_cols: int = 5, 
        data_types: Optional[List[str]] = None,
        include_headers: bool = True,
        seed: Optional[int] = None
    ) -> List[List[Any]]:
        """
        Generate a table with random data based on specified parameters.
        
        Args:
            num_rows: Number of data rows to generate
            num_cols: Number of columns to generate
            data_types: List of data types for columns (if None, random types will be chosen)
            include_headers: Whether to include header row
            seed: Random seed for reproducibility
            
        Returns:
            A list of lists representing the table data
        """
        # Set random seed if provided
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Generate or use provided data types
        if data_types is None or len(data_types) != num_cols:
            data_types = [random.choice(cls.DATA_TYPES) for _ in range(num_cols)]
        
        # Generate column headers
        headers = []
        for i, dtype in enumerate(data_types):
            if dtype in cls.COLUMN_NAMES:
                column_name = random.choice(cls.COLUMN_NAMES[dtype])
                # Avoid duplicate column names
                while column_name in headers:
                    column_name = f"{column_name}_{i+1}"
                headers.append(column_name)
            else:
                headers.append(f"column_{i+1}")
        
        # Initialize table with headers if requested
        table = []
        if include_headers:
            table.append(headers)
        
        # Generate data rows
        for _ in range(num_rows):
            row = []
            for dtype in data_types:
                row.append(cls._generate_value_for_type(dtype))
            table.append(row)
        
        return table

    @classmethod
    def _generate_value_for_type(cls, data_type: str) -> Any:
        """
        Generate a random value for the specified data type.
        
        Args:
            data_type: The type of data to generate
            
        Returns:
            A random value of the specified type
        """
        if data_type == "string":
            return ''.join(random.choices(string.ascii_letters + ' ', k=random.randint(5, 15))).strip()
        
        elif data_type == "integer":
            return random.randint(1, 1000)
        
        elif data_type == "float":
            return round(random.uniform(1.0, 100.0), 2)
        
        elif data_type == "date":
            start_date = datetime(2020, 1, 1)
            days = random.randint(0, 1095)  # Up to ~3 years from start date
            return (start_date + timedelta(days=days)).strftime('%Y-%m-%d')
        
        elif data_type == "boolean":
            return random.choice([True, False])
        
        elif data_type == "email":
            domains = ["example.com", "test.org", "company.net", "mail.co"]
            username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            domain = random.choice(domains)
            return f"{username}@{domain}"
        
        elif data_type == "name":
            first_names = ["John", "Jane", "Alice", "Bob", "Maria", "David", "Sarah", "Michael"]
            last_names = ["Smith", "Johnson", "Brown", "Lee", "Garcia", "Miller", "Davis", "Wilson"]
            return f"{random.choice(first_names)} {random.choice(last_names)}"
        
        elif data_type == "address":
            streets = ["Main St", "Oak Ave", "Park Rd", "Maple Ln", "Cedar Blvd"]
            cities = ["Springfield", "Rivertown", "Oakville", "Maplewood", "Franklin"]
            return f"{random.randint(100, 999)} {random.choice(streets)}, {random.choice(cities)}"
        
        elif data_type == "product":
            adjectives = ["Premium", "Deluxe", "Basic", "Advanced", "Smart", "Ultra"]
            products = ["Widget", "Gadget", "Tool", "Device", "System", "Solution"]
            return f"{random.choice(adjectives)} {random.choice(products)}"
        
        elif data_type == "price":
            return f"${round(random.uniform(9.99, 499.99), 2)}"
        
        else:
            # Default to string for unknown types
            return f"Sample-{random.randint(1000, 9999)}"

    @classmethod
    def table_to_csv_string(cls, table: List[List[Any]]) -> str:
        """
        Convert a table (list of lists) to a CSV string.
        
        Args:
            table: The table data as a list of lists
            
        Returns:
            CSV formatted string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(table)
        return output.getvalue()

    @classmethod
    def table_to_csv_bytes(cls, table: List[List[Any]]) -> bytes:
        """
        Convert a table (list of lists) to CSV bytes.
        
        Args:
            table: The table data as a list of lists
            
        Returns:
            CSV formatted bytes
        """
        return cls.table_to_csv_string(table).encode('utf-8')
        
    @classmethod
    def table_to_json(cls, table: List[List[Any]]) -> List[Dict[str, Any]]:
        """
        Convert a table (list of lists) to JSON format.
        
        Args:
            table: The table data as a list of lists
            
        Returns:
            List of dictionaries representing the table in JSON format
        """
        if not table or len(table) < 2:
            return []
            
        headers = table[0]
        rows = table[1:]
        
        json_data = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                if i < len(headers):  # Ensure we don't go out of bounds
                    row_dict[headers[i]] = value
            json_data.append(row_dict)
            
        return json_data
        
    @classmethod
    def table_to_json_string(cls, table: List[List[Any]]) -> str:
        """
        Convert a table (list of lists) to a JSON string.
        
        Args:
            table: The table data as a list of lists
            
        Returns:
            JSON formatted string
        """
        import json
        json_data = cls.table_to_json(table)
        return json.dumps(json_data, indent=2)
        
    @classmethod
    def table_to_json_bytes(cls, table: List[List[Any]]) -> bytes:
        """
        Convert a table (list of lists) to JSON bytes.
        
        Args:
            table: The table data as a list of lists
            
        Returns:
            JSON formatted bytes
        """
        return cls.table_to_json_string(table).encode('utf-8')

    @classmethod
    def table_to_dataframe(cls, table: List[List[Any]], has_header: bool = True) -> pd.DataFrame:
        """
        Convert a table (list of lists) to a pandas DataFrame.
        
        Args:
            table: The table data as a list of lists
            has_header: Whether the first row contains headers
            
        Returns:
            pandas DataFrame
        """
        if has_header:
            headers = table[0]
            data = table[1:]
            return pd.DataFrame(data, columns=headers)
        else:
            return pd.DataFrame(table)

    @classmethod
    def generate_sample_csv(cls, sample_type: str, rows: int = 100) -> bytes:
        """
        Generate a sample CSV file of the specified type.
        
        Args:
            sample_type: Type of sample to generate (users, products, transactions)
            rows: Number of rows to generate
            
        Returns:
            CSV formatted bytes
        """
        if sample_type == "users":
            data_types = ["integer", "name", "email", "date", "boolean"]
            headers = ["id", "full_name", "email", "registration_date", "is_active"]
        
        elif sample_type == "products":
            data_types = ["integer", "product", "price", "integer", "boolean"]
            headers = ["id", "product_name", "price", "stock", "in_stock"]
        
        elif sample_type == "transactions":
            data_types = ["integer", "integer", "date", "price", "string"]
            headers = ["id", "user_id", "transaction_date", "amount", "status"]
        
        else:
            # Default to a generic table
            return cls.table_to_csv_bytes(cls.generate_table_data(num_rows=rows, num_cols=5))
        
        # Generate data with specific headers
        table = [headers]
        for _ in range(rows):
            row = []
            for dtype in data_types:
                row.append(cls._generate_value_for_type(dtype))
            table.append(row)
        
        return cls.table_to_csv_bytes(table)

    @classmethod
    def analyze_csv(cls, csv_content: Union[str, bytes]) -> Dict[str, Any]:
        """
        Analyze a CSV file and return statistics.
        
        Args:
            csv_content: The CSV content as string or bytes
            
        Returns:
            Dictionary of statistics about the CSV
        """
        try:
            # Convert bytes to string if needed
            if isinstance(csv_content, bytes):
                csv_content = csv_content.decode('utf-8')
            
            # Parse CSV with pandas
            df = pd.read_csv(io.StringIO(csv_content))
            
            # Generate basic statistics
            stats = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": df.columns.tolist(),
                "column_types": {col: str(df[col].dtype) for col in df.columns},
                "memory_usage": df.memory_usage(deep=True).sum(),
                "sample_rows": df.head(5).to_dict(orient='records')
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error analyzing CSV: {str(e)}")
            raise ValueError(f"Error analyzing CSV: {str(e)}")
        
    @classmethod
    def table_to_json_response(cls, table: List[List[Any]]) -> Dict[str, Any]:
        """
        Convert a table (list of lists) to a structured JSON response with metadata.
        
        Args:
            table: The table data as a list of lists
            
        Returns:
            Dictionary with metadata and data ready for JSON serialization
        """
        if not table or len(table) < 2:
            return {"metadata": {"rows": 0, "columns": 0, "headers": []}, "data": []}
        
        headers = table[0]
        json_data = cls.table_to_json(table)
        
        return {
            "metadata": {
                "rows": len(table) - 1,  # Subtract header row
                "columns": len(headers),
                "headers": headers
            },
            "data": json_data
        }

    @classmethod
    def generate_sample_json(cls, sample_type: str, rows: int = 100) -> Dict[str, Any]:
        """
        Generate a sample dataset in JSON format.
        
        Args:
            sample_type: Type of sample to generate (users, products, transactions)
            rows: Number of rows to generate
            
        Returns:
            Dictionary with metadata and data ready for JSON serialization
        """
        if sample_type == "users":
            data_types = ["integer", "name", "email", "date", "boolean"]
            headers = ["id", "full_name", "email", "registration_date", "is_active"]
        
        elif sample_type == "products":
            data_types = ["integer", "product", "price", "integer", "boolean"]
            headers = ["id", "product_name", "price", "stock", "in_stock"]
        
        elif sample_type == "transactions":
            data_types = ["integer", "integer", "date", "price", "string"]
            headers = ["id", "user_id", "transaction_date", "amount", "status"]
        
        else:
            # Default to a generic table
            return cls.table_to_json_response(cls.generate_table_data(num_rows=rows, num_cols=5))
        
        # Generate data with specific headers
        table = [headers]
        for _ in range(rows):
            row = []
            for dtype in data_types:
                row.append(cls._generate_value_for_type(dtype))
            table.append(row)
        
        return cls.table_to_json_response(table)