import os
from fastapi import FastAPI 
from auth_server.routes import clients 
from dotenv import load_dotenv




load_dotenv() # load all the .env args in this session memory

# we need to save the key pairs private_key must be save in the .env file and all shit  or whatever  if  there is not private_key  availabe and also we have to make sure for the public key also 

# so whenever we strart the server again then it picksup nicely , if it is not there then  with the creation logic we would create that without having any problem 

# i also need to instantiate the  create all db tables and all objects structurs  when the server will start 

def create_app():

    app = FastAPI(title="OAuth")

    # include all other routes here 
    app.include_router(clients.router)


    if os.environ.get("PRIVATE_KEY") == '' :
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        


        def key_pair_generation() -> tuple[str,str]:
            # these key generation part is most likely i dont know so i have taken some help albeit these part is like two asymetric key will be 
            # used where one will be used to signe (which is private key ) given to the user and   now to verify the digest something like 
            # 
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )

            public_key =  private_key.public_key()

            private_key_text=  private_key.private_bytes(
                encoding= serialization.Encoding.PEM,
                format= serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')

            public_key_text =  public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')



            return (public_key_text, private_key_text)



        publicKey, privateKey = key_pair_generation()

        
        # my though process is like it is better to save that and we can reuse if we restart the server not generating freshones 
        # guys who think we still for the security once in a while have to make sure have refresh those thing , even though by all means
        # i say it is very hard to guess but still we can have  cron job or something  that will ran and populate the .env file or replace particular shit using sed command  there can be manny good ways  butyeah  this is the one i think is well to go 


        with open(".env","a+") as env_file:
            written_n = env_file.write(f"PRIVATE_KEY={privateKey}\nPUBLIC_KEY={publicKey}")
            
            try:
                if written_n==0:
                    raise ValueError("Write Error")
            finally:
                pass

        # load it again
        _ = load_dotenv()
        
    else:
        # here we dont need anything do we 
        privateKey= os.environ.get("PRIVATE_KEY")

    return app


app = create_app()
