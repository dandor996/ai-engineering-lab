import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from config.settings import Settings

security = HTTPBearer()

def verify_token(user = Depends(security)):
    settings = Settings()
    try:
        payload = jwt.decode(user.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
