from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
        
from dotenv import set_key


def key_pair_generation() -> tuple[str,str]:

    # these key generation part is most likely i dont know so i have taken some help albeit these part is like two asymetric key will be 
    # used where one will be used to signe (which is private key ) given to the user and   now to verify the digest something like 
      
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    publicKey =  privateKey.public_key()

    private_key_text=  privateKey.private_bytes(
        encoding= serialization.Encoding.PEM,
        format= serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_key_text =  publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return private_key_text, public_key_text



def save_key_pair(private_key: str, public_key: str) -> None:
    set_key(
        ".env",
        "PRIVATE_KEY",
        private_key.replace("\n", "\\n"),
    )

    set_key(
        ".env",
        "PUBLIC_KEY",
        public_key.replace("\n", "\\n"),
    )
