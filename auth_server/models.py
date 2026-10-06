from datetime import UTC, datetime
from sqlalchemy import  DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship,Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from auth_server.database import Base

class Client(Base):
    __tablename__='client'
   
    client_id                   :Mapped[int]        = mapped_column(Integer, primary_key=True)
    client_secret               :Mapped[str]        = mapped_column(String(255),nullable=False)
    client_id_issued_at         :Mapped[datetime]   = mapped_column(DateTime(timezone=True),default = lambda : datetime.now())
    client_secret_expires_at    :Mapped[datetime]   = mapped_column(DateTime(),default = 0)
    client_name                 :Mapped[str]        = mapped_column(String(60),nullable=False)
    grant_type                  :Mapped[list[str]]  = mapped_column(ARRAY(String),nullable=False)
    client_type                 :Mapped[str]        = mapped_column(String(60),nullable=False)
    redirect_uris               :Mapped[str]        = mapped_column(String(255))

    auth_detail                                     = relationship("AuthDetail",backref="client",lazy=True)

class AuthToken(Base):
    __tablename__ = 'auth_detail'

    auth_id   = mapped_column(Integer,primary_key=True)
    jwt_token = mapped_column(Integer,primary_key=True)
    client_id = mapped_column(Integer,ForeignKey('client.client_id'),nullable=False) 
