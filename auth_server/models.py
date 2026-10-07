from datetime import  datetime
from sqlalchemy import  DateTime, ForeignKey, Integer, String,JSON
from sqlalchemy.orm import relationship,Mapped, mapped_column
from auth_server.database import Base

class Client(Base):
    __tablename__:str='client'
   
    client_id                   :Mapped[str]        = mapped_column(String, primary_key=True)
    client_secret               :Mapped[str]        = mapped_column(String(255),nullable=False)
    client_id_issued_at         :Mapped[datetime]   = mapped_column(DateTime(timezone=True),default = lambda : datetime.now())
    client_secret_expires_at    :Mapped[datetime]   = mapped_column(DateTime(timezone=True),nullable=True,default = None) # default also has to be of that object type or what cause currently i have given is the integer and all . 
    client_name                 :Mapped[str]        = mapped_column(String(60),nullable=False)
    grant_types                  :Mapped[list[str]]  = mapped_column(JSON,nullable=False)
    client_type                 :Mapped[str]        = mapped_column(String(60),nullable=False)
    redirect_uris               :Mapped[str]        = mapped_column(String(255),nullable=True)

    auth_detail                                     = relationship("AuthToken",backref="client",lazy=True)

class AuthToken(Base):
    __tablename__ :str = 'auth_detail'

    auth_id   :Mapped[int]  = mapped_column(Integer,primary_key=True)
    jwt_token :Mapped[str]  = mapped_column(String,primary_key=True)
    client_id :Mapped[str]  = mapped_column(Integer,ForeignKey('client.client_id'),nullable=False) 
