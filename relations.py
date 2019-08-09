from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base #import the declarative base for getting the base class for the user classes that will be mapped against the database tables

engine = create_engine("sqlite:///:memory:",echo=True) #create the inmemory sqlite database reference to connect, echo to log the sql statements which is better for learning

Base = declarative_base() #metadata of the table automaically created by the declarative base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nick_name = Column(String) 
    full_name = Column(String)
    #for backward relation ship of the User to the address
    addresses = relationship("Address",back_populates="user")

    def __repr__(self):
        return "<User(name=%s, full_name=%s, nick_name=%s)>" % (self.name, self.full_name, self.nick_name)

class Address(Base):
    __tablename__ = "addresses"
    id= Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("users.id"))
    email_address = Column(String,nullable=False)
    #for backward relation ship of the Address class to the User class
    user = relationship("User",back_populates="addresses")
    def __repr__(self):
        return "<Address(email=%s)>"%self.email_address

#creating the non existing tables in the database
#we use the metadata attribute of our declarative base class to create the non existing tables
Base.metadata.create_all(engine) #we have to provide the engine of the database as a reference we want to refer to

#the __init__() method
#
#Our User class, as defined using the Declarative system, has been provided with a constructor (e.g. __init__() method) which automatically accepts keyword names that match the columns we’ve mapped. We are free to define any explicit __init__() method we prefer on our class, which will override the default method provided by Declarative.

#orm will talk to the database using the Session handle. Here is How. Whenever we need to do something in the database we need a Session object to that database

#either use
# Session = sessionmaker(bind=engine) #or we can use

Session = sessionmaker() #we define a Session class which will be used as the factory to create the session objects
Session.configure(bind=engine) #engine already created earlier, now configure the session to use that engine

#create a session
session = Session()
#add the user to the database, basically the insert command

foo_user = User(name="foo", full_name="foo_bar",nick_name="foo_bar_nick_name")

#now adding the addresses to the user foo

foo_user.addresses = [
Address(email_address="foo@hotmail.com"),
Address(email_address="foobar@hitmail.com"),
]

#adding the changes to the database
session.add(foo_user)
session.commit()

#filter the user foo and get it addresses
foo = session.query(User).filter_by(name="foo").first()
print("foo: %s"%foo)
print("foo addresses: %s"%foo.addresses)
