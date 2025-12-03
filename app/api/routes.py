#FASTAPI RESTAPI ROUTES - simple config validation endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.core.validator import ConfigValidator

router = APIRouter()
validator = ConfigValidator()

class ValidateRequest(BaseModel):
    config_type: str  # "json" or "yaml"
    config_content: str

class ValidateResponse(BaseModel):
    valid: bool
    errors: List[str]
    message: str

@router.get("/health")
async def health_check():
    # Simple health check endpoint
    return {"status": "ok", "service": "config-validator"}

@router.post("/validate", response_model=ValidateResponse)
async def validate_config(request: ValidateRequest):
   # validate a single config file (JSON or YAML)
    try:
        is_valid, errors = validator.validate_content(
            request.config_content, 
            request.config_type
        )

        return ValidateResponse(
            valid=is_valid,
            errors=errors,
            message="Validation successful" if is_valid else "Validation failed"
        )
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/validate-files")
async def validate_config_files():
    # Validate all config files found inside configs folder and return summary
    try:
        results = validator.validate_all_configs()
        all_valid = all(result.get("valid", False) for result in results)

        return {
            "all_valid": all_valid,
            "results": results,
            "total_files": len(results),
            "failed_files": sum(1 for r in results if not r["valid"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))