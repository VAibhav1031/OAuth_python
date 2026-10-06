import os
from auth_server.utils import key_pair_generation, save_key_pair

class Setting:
    def __init__(self):
        self.database_url=os.getenv("DATABASE_URL","sqlite:///./test.db")

        private_key = os.getenv("PRIVATE_KEY")
        public_key = os.getenv("PUBLIC_KEY")

        if private_key is None and public_key is None:
            private_key , public_key =  key_pair_generation()
            # must save things in the .env  file
            save_key_pair(private_key,public_key) 
        
        elif private_key is None or  public_key is None:
            return RuntimeError("Both PRIVATE_KEY and PUBLIC_KEY  must be available or both be absent")


        self.private_key=private_key.replace("\\n","\n")
        self.public_key=public_key.replace("\\n","\n")


setting=Setting()

