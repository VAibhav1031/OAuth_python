from fastapi import FastAPI 
from auth_server.routes import clients 

def create_app():

    app = FastAPI(title="OAuth")

    # include all other routers here 
    app.include_router(clients.router)
    
    return app

app = create_app()

@app.get("/")
async def rootHandle():
    return {"message":"Healthy"}
