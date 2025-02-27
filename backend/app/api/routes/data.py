"""
API routes for versatile data generation in multiple formats
"""
import json
import logging
from typing import List, Dict, Any, Optional, Union

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Query, Header, Response
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io

from app.api.dependencies import request_audit_log, APIVersion
from app.api.utils.table_processor import TableProcessor


# Create logger
logger = logging.getLogger("app")

# Create router
router = APIRouter(
    prefix="/api/data",
    tags=["data-generation"],
    dependencies=[Depends(request_audit_log)],
)


@router.get("/generate", status_code=status.HTTP_200_OK)
async def generate_data(
    rows: int = Query(10, ge=1, le=1000, description="Number of rows to generate"),
    columns: int = Query(10, ge=1, le=20, description="Number of columns to generate"),
    data_types: Optional[List[str]] = Query(None, description="List of data types for columns"),
    format: Optional[str] = Query(None, description="Output format override (csv or json)"),
    accept: Optional[str] = Header(None, description="Accept header for content negotiation")
) -> Response:
    """
    Generate data with random values based on specified parameters.
    Response format is determined by the format parameter or Accept header.
    
    Args:
        rows: Number of rows to generate
        columns: Number of columns to generate
        data_types: Optional list of data types for columns
        format: Optional format override (csv or json)
        accept: HTTP Accept header
        
    Returns:
        Data in the requested format
    """
    try:
        # Validate data types if provided
        if data_types:
            for dt in data_types:
                if dt not in TableProcessor.DATA_TYPES:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid data type: {dt}. Valid types are: {TableProcessor.DATA_TYPES}"
                    )
        
        # Generate table data
        table_data = TableProcessor.generate_table_data(
            num_rows=rows,
            num_cols=columns,
            data_types=data_types
        )
        
        # Determine output format (default to json)
        output_format = "json"
        
        # If format parameter is provided, it overrides Accept header
        if format is not None:
            format = format.lower()
            if format in ["csv", "json"]:
                output_format = format
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid format: {format}. Supported formats are: csv, json"
                )
        # Otherwise, use Accept header for content negotiation
        elif accept is not None and "text/csv" in accept:
            output_format = "csv"
        
        # Return based on determined format
        if output_format == "csv":
            # Convert to CSV bytes
            csv_bytes = TableProcessor.table_to_csv_bytes(table_data)
            
            # Return as downloadable file
            return StreamingResponse(
                io.BytesIO(csv_bytes),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=generated_data_{rows}x{columns}.csv"
                }
            )
        else:  # output_format == "json"
            # Convert to JSON-ready dictionary
            json_response = TableProcessor.table_to_json_response(table_data)
            
            # Return JSON response
            return JSONResponse(content=json_response)
            
    except Exception as e:
        logger.error(f"Error generating data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating data: {str(e)}"
        )


@router.get("/sample/{sample_type}", status_code=status.HTTP_200_OK)
async def get_sample_data(
    sample_type: str,
    rows: int = Query(100, ge=1, le=1000, description="Number of rows to generate"),
    format: Optional[str] = Query(None, description="Output format override (csv or json)"),
    accept: Optional[str] = Header(None, description="Accept header for content negotiation")
) -> Response:
    """
    Get a sample dataset of the specified type.
    Response format is determined by the format parameter or Accept header.
    
    Args:
        sample_type: Type of sample (users, products, transactions)
        rows: Number of rows to generate
        format: Optional format override (csv or json)
        accept: HTTP Accept header
        
    Returns:
        Sample data in the requested format
    """
    valid_types = ["users", "products", "transactions"]
    
    if sample_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sample type. Valid types are: {valid_types}"
        )
    
    try:
        # Determine output format (default to json)
        output_format = "json"
        
        # If format parameter is provided, it overrides Accept header
        if format is not None:
            format = format.lower()
            if format in ["csv", "json"]:
                output_format = format
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid format: {format}. Supported formats are: csv, json"
                )
        # Otherwise, use Accept header for content negotiation
        elif accept is not None and "text/csv" in accept:
            output_format = "csv"
        
        # Return based on determined format
        if output_format == "csv":
            # Generate sample CSV
            csv_bytes = TableProcessor.generate_sample_csv(sample_type, rows)
            
            # Return as downloadable file
            return StreamingResponse(
                io.BytesIO(csv_bytes),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={sample_type}_sample.csv"
                }
            )
        else:  # output_format == "json"
            # Generate sample JSON
            json_data = TableProcessor.generate_sample_json(sample_type, rows)
            
            # Return JSON response
            return JSONResponse(content=json_data)
            
    except Exception as e:
        logger.error(f"Error generating sample data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating sample data: {str(e)}"
        )


@router.get("/sample", status_code=status.HTTP_200_OK)
async def get_sample_info() -> Dict[str, Any]:
    """
    Get information about available sample datasets.
    
    Returns:
        Dictionary with sample information
    """
    return {
        "message": "Sample data endpoint",
        "available_samples": [
            "users", 
            "products",
            "transactions"
        ],
        "formats": ["csv", "json"],
        "usage": "Use /api/data/sample/{sample_type}?format=csv to download a specific sample"
    }


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    api_version: APIVersion = None
) -> Dict[str, Any]:
    """
    Upload and analyze a data file (CSV or JSON).
    
    Args:
        file: The file to upload
        api_version: The current API version
        
    Returns:
        A dictionary with information about the processed file
    """
    if not (file.filename.endswith('.csv') or file.filename.endswith('.json')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a CSV or JSON file"
        )
    
    try:
        # Read file content
        contents = await file.read()
        
        # Process based on file type
        if file.filename.endswith('.csv'):
            # Use TableProcessor to analyze the CSV
            stats = TableProcessor.analyze_csv(contents)
        else:  # JSON file
            # Parse JSON and convert to a basic structure
            try:
                json_data = json.loads(contents.decode('utf-8'))
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid JSON file"
                )
            
            # Handle different possible JSON structures
            if isinstance(json_data, list):
                # Assume array of objects
                if json_data and isinstance(json_data[0], dict):
                    stats = {
                        "row_count": len(json_data),
                        "column_count": len(json_data[0]) if json_data else 0,
                        "columns": list(json_data[0].keys()) if json_data else [],
                        "sample_rows": json_data[:5] if len(json_data) > 5 else json_data
                    }
                else:
                    stats = {"data": json_data}
            elif isinstance(json_data, dict):
                # Handle object with data array
                if "data" in json_data and isinstance(json_data["data"], list):
                    stats = {
                        "row_count": len(json_data["data"]),
                        "metadata": json_data.get("metadata", {}),
                        "sample_rows": json_data["data"][:5] if len(json_data["data"]) > 5 else json_data["data"]
                    }
                else:
                    stats = json_data
            else:
                stats = {"data": json_data}
        
        # Add additional information
        stats["filename"] = file.filename
        stats["file_type"] = "csv" if file.filename.endswith('.csv') else "json"
        stats["api_version"] = api_version
        
        logger.info(f"Successfully processed file: {file.filename}")
        return stats
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )