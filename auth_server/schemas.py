from pydantic import BaseModel

# These are for the incoming http request body primarily of JSON type .... 
# need to specify what is required and what is not required 
class ClientDet(BaseModel):
    client_name: str 
    grant_types: list[str]
    client_type: str
    redirect_uris: list[str] | None= None

class AuthDet(BaseModel):
    client_id: str
    client_secret: str
    client_type: str
    grant_type: str
    redirect_uris: list[str] | None = None

