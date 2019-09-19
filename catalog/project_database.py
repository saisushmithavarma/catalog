from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base=declarative_base()


class Register(Base):#Base creates database 
	__tablename__='register'#name of the table

	id=Column(Integer,primary_key=True)
	name=Column(String(100))
	surname=Column(String(100))
	mobile=Column(String(50))
	email=Column(String(50))
	branch=Column(String(10))
	role=Column(String(50))

class User(Base,UserMixin):
	__tablename__='User'
	id=Column(Integer,primary_key=True)
	name=Column(String(100),nullable=False)
	email=Column(String(100),nullable=False)
	password=Column(String(100),nullable=False)
	


engine=create_engine('sqlite:///iii.db')#Format
Base.metadata.create_all(engine)#database will be present in engine,Metadata means the data which is sent to browser
print("Database is created......")
