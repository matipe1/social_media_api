from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "9703f94560d1a215bf5981720bf26493e5166ddba67d871b338c0cb0b5de904ff0f53a81ec63e96413f3eb8080958dcb67943d4160d39c0d6f5b27e20d84b1ee2ae67cde10756e0f3d9c214e64e93ea2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) # [ALGORITHM]
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)