from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.domain.exceptions import InvalidFeatureError, PredictionTimeoutError, DomainException

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DomainException, _domain_exception_handlers)

async def _domain_exception_handlers(
    request: Request,
    exc: DomainException) -> JSONResponse:

    if isinstance(exc, InvalidFeatureError):
        details = {
            "code": 422,
            "message": 'Invalid feature(s) provided. Please check the payload.'
        }
    elif isinstance(exc, PredictionTimeoutError):
        details = {
            "code": 504,
            "message": 'Prediction request timeout. Please try again later.'
        }
    else:
        details = {
            "code": 400,
            "message": 'Generic Error'   
        } 
    return JSONResponse(status_code=details['code'], content={'error': details['message'], 'details': str(exc)})
    

