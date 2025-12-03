"""
FastAPI application entrypoint for the Config Validator Service.
"""
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Config Validator Service",
    description="A service to validate JSON and YAML configuration files",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)