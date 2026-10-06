import jwt
import bcrypt
from fastapi import HTTPException, status
from datetime import datetime, timedelta,UTC


def jwtCreation(client_id:str,private_key:str):
    payload = {
        "client_id":client_id,
        "exp":datetime.now(UTC) + timedelta(minutes=5) 
    }
    
    return jwt.encode(payload=payload,key=private_key,algorithm="RSA256")


def jwtVerification(token:str,public_key:str):
    
    try:
        payload = jwt.decode(token,public_key,algorithms="RSA256")
        
        client_id = payload.get("client_id")
        if client_id == "":
            raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate credentials",
                headers={"WWW-Authenticate":"Bearer"}
            )

        return client_id
        

    except jwt.ExpiredSignatureError:
        raise HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has Expired",
        headers={"WWW-Authenticate":"Bearer"}
        )


    except jwt.InvalidTokenError:
        raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate credentials",
                headers={"WWW-Authenticate":"Bearer"}
        )

def hashPassword(password:str):
    password_byte = password.encode(encoding='utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_byte,salt)

    return hashed_password

def verifyHashedPassword(password:str, hashPassword:bytes):
    password_byte = password.encode(encoding='utf-8')

    return bcrypt.checkpw(password_byte,hashPassword)
     
