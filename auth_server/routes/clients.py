import secrets
from fastapi import Depends,APIRouter, HTTPException, status
from sqlalchemy import select
from .routes_helper import hashPassword, jwtCreation, verifyHashedPassword
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from auth_server.config import setting 
from auth_server.schemas import AuthDet, ClientDet
from auth_server.database import get_db
from auth_server.models import Client,AuthToken


router = APIRouter(prefix="/api/v1", tags=["Users"])

@router.post("/register-client")
async def registerClient(payload: ClientDet,db:Session=Depends(get_db)):

    # if payload.client_type == 'confedential': # if it is the  confedential then we have to use something differnet else nope
    client_id = "client" + secrets.token_hex(8)[2:] # removing sec  part
    client_secret =  secrets.token_hex(32)

    hashed_client_secret = hashPassword(client_secret) 
    client = Client(client_id=client_id, client_secret=hashed_client_secret,client_name=payload.client_name,client_type=payload.client_type)
    
    try:
        db.add(client)
        db.commit()
    except SQLAlchemyError:
       return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"messasge":"internal_server_error"}
        ) 
    

    return JSONResponse(
            status_code=status.HTTP_201_CREATED,        
            content={"client_id":client_id,"secret": client_secret}
        )

@router.post("/oauth/token")
async def oauth_token(payload: AuthDet,db:Session=Depends(get_db)):
    # must verify is it for what like is it for the client_credentials or , refresh tokens or what 
   
    # verifcation first mann 
    stmt = select(Client).where(Client.client_id==payload.client_id,Client.client_secret==payload.client_secret)
    
    client_re = db.scalars(stmt).first()
    if client_re is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal_server_error"
        )

    c_secret = client_re.client_secret.encode(encoding='utf-8')
    
    if not verifyHashedPassword(payload.client_secret,c_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client-credentials"
        )

    if payload.grant_type=='client_credentials':
        jwtToken = jwtCreation(payload.client_id,setting.private_key) 
       
        auth =AuthToken(client_id=payload.client_id,jwt_token=jwtToken)
        try:
            db.add(auth)
            db.commit()
        except SQLAlchemyError:
           return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"messasge":"internal_server_error"}
            ) 
   
        # everything gone as perfect
        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"token":jwtToken},
                )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="grant-type not found"
                )


@router.get("/.well-known/jwks.json")
async def getPublicKey():
    return JSONResponse(status_code=status.HTTP_200_OK,content={"public_key":setting.public_key})
