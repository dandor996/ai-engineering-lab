from fastapi import FastAPI
from config.logging import setup_logging
from api.exceptions import register_exception_handlers
from api.routers.inference import router as inference_router

setup_logging()
app = FastAPI(title="FastAPI Skeleton", version="0.1.0")
register_exception_handlers(app)
app.include_router(inference_router, prefix="/api/v1", tags=["predictions"])

