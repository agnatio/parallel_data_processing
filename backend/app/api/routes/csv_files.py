"""
API routes for handling CSV files
"""
import logging
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Query
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io

from app.api.dependencies import request_audit_log, APIVersion
from app.api.utils.table_processor import TableProcessor


# Create logger
logger = logging.getLogger("app")

# Create router
router = APIRouter(
    prefix="/api/csv",
    tags=["csv-files"],
    dependencies=[Depends(request_audit_log)],
)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_csv(
    file: UploadFile = File(...),
    api_version: APIVersion = None
) -> Dict[str, Any]:
    """
    Upload and process a CSV file.
    
    Args:
        file: The CSV file to upload
        api_version: The current API version
        
    Returns:
        A dictionary with information about the processed CSV
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a CSV"
        )
    
    try:
        # Read CSV content
        contents = await file.read()
        
        # Use TableProcessor to analyze the CSV
        stats = TableProcessor.analyze_csv(contents)
        
        # Add additional information
        stats["filename"] = file.filename
        stats["api_version"] = api_version
        
        logger.info(f"Successfully processed CSV file: {file.filename}")
        return stats
    
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CSV file: {str(e)}"
        )


@router.get("/generate", status_code=status.HTTP_200_OK)
async def generate_csv(
    rows: int = Query(10, ge=1, le=1000, description="Number of rows to generate"),
    columns: int = Query(10, ge=1, le=20, description="Number of columns to generate"),
    data_types: Optional[List[str]] = Query(None, description="List of data types for columns")
) -> StreamingResponse:
    """
    Generate a CSV file with random data.
    
    Args:
        rows: Number of rows to generate
        columns: Number of columns to generate
        data_types: Optional list of data types for columns
        
    Returns:
        Streaming response with the generated CSV file
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
    
    except Exception as e:
        logger.error(f"Error generating CSV: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating CSV: {str(e)}"
        )


@router.get("/sample", status_code=status.HTTP_200_OK)
async def get_sample_csv_info() -> Dict[str, Any]:
    """
    Get information about generating sample CSV files.
    
    Returns:
        A dictionary with sample CSV information
    """
    return {
        "message": "Sample CSV endpoint",
        "available_samples": [
            "users", 
            "products",
            "transactions"
        ],
        "usage": "Use /api/csv/sample/{sample_name} to download a specific sample"
    }


@router.get("/sample/{sample_type}", status_code=status.HTTP_200_OK)
async def get_sample_csv(
    sample_type: str,
    rows: int = Query(100, ge=1, le=1000, description="Number of rows to generate")
) -> StreamingResponse:
    """
    Get a sample CSV file of the specified type.
    
    Args:
        sample_type: Type of sample (users, products, transactions)
        rows: Number of rows to generate
        
    Returns:
        Streaming response with the sample CSV file
    """
    valid_types = ["users", "products", "transactions"]
    
    if sample_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sample type. Valid types are: {valid_types}"
        )
    
    try:
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
    
    except Exception as e:
        logger.error(f"Error generating sample CSV: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating sample CSV: {str(e)}"
        )