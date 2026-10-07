from pydantic import BaseModel

# These are for the incoming http request body primarily of JSON type .... 
# need to specify what is required and what is not required 
class ClientDet(BaseModel):
    client_name: str 
    grant_types: list[str]
    client_type: str
    redirect_uris: list[str] | None= None


# oauth/token has many type based on teh grant_type we have different approach to the verify ourselves

#client_credentials
class AuthDetClientCredentials(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    scope:str | None = None


#authorization_code
class AuthDetAuthorizationCode(BaseModel):
    grant_type: str
    code: str | None = None
    redirect_uri:str | None = None
    client_id:str 
    client_secret:str
    code_verifier:str | None = None

#refresh_token
class AuthDetRefreshToken(BaseModel):
    grant_type:str
    refrest_token:str
    client_id:str
    client_secret:str

