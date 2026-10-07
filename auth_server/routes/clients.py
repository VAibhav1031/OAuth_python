import secrets
from fastapi import Depends,APIRouter, HTTPException, Request, status
from sqlalchemy import select
from starlette.status import HTTP_400_BAD_REQUEST
from .routes_helper import hashPassword, jwtCreation, verifyHashedPassword
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from auth_server.config import setting 
from auth_server.schemas import AuthDetAuthorizationCode, AuthDetClientCredentials, AuthDetRefreshToken, ClientDet
from auth_server.database import get_db
from auth_server.models import Client,AuthToken


router = APIRouter(prefix="/api/v1", tags=["Clients"])

@router.post("/register-client")
async def registerClient(payload: ClientDet,db:Session=Depends(get_db)):

    # if payload.client_type == 'confedential': # if it is the  confedential then we have to use something differnet else nope
    client_id = "client_" + secrets.token_hex(8)[2:] # removing sec  part
    client_secret =  secrets.token_hex(32)

    hashed_client_secret = hashPassword(client_secret) 
    client = Client(client_id=client_id, client_secret=hashed_client_secret,client_name=payload.client_name,grant_types=payload.grant_types,client_type=payload.client_type)
    
    try:
        db.add(client)
        db.commit()
    except SQLAlchemyError as exc:
        print("Error: ",exc)
        db.rollback()

        # return JSONResponse(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,        
        #         content={"message":"internal_server_error"}
        #     )
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="internal_server_error"
            )

    return JSONResponse(
            status_code=status.HTTP_201_CREATED,        
            content={"client_id":client_id,"secret": client_secret}
        )

@router.post("/oauth/token")
async def oauth_token(request:Request,db:Session=Depends(get_db)):
    # must verify is it for what like is it for the client_credentials or , refresh tokens or what 
    
    data  = await request.json()

    grant_type = data.get("grant_type") 

    if grant_type == "client_credentals":
        body = AuthDetClientCredentials.model_validate(data)

    elif grant_type == "authorization_token":
        body = AuthDetAuthorizationCode.model_validate(data)
        handle_authorization_code(db,body)
    elif grant_type == "refresh_token":
        body = AuthDetRefreshToken.model_validate(data)
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="unkown grant_type"
            )
   

def handle_authorization_code(db:Session,data):
    # verifcation first mann 
    stmt = select(Client).where(Client.client_id==data.client_id,Client.client_secret==data.client_secret)
    
    client_re = db.scalars(stmt).first()
    if client_re is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal_server_error"
        )

    c_secret = client_re.client_secret.encode(encoding='utf-8')
    
    if not verifyHashedPassword(data.client_secret,c_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client-credentials"
        )

    jwtToken = jwtCreation(data.client_id,setting.private_key) 
   
    auth =AuthToken(client_id=data.client_id,jwt_token=jwtToken)
    try:
        db.add(auth)
        db.commit()
    except InvalidRequestError:
       return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"messasge":"internal_server_error"}
        ) 

    # everything gone as perfect
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"token":jwtToken},
            )
    


@router.get("/.well-known/jwks.json")
async def getPublicKey():
    return JSONResponse(status_code=status.HTTP_200_OK,content={"public_key":setting.public_key})
