from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base #import the declarative base for getting the base class for the user classes that will be mapped against the database tables

engine = create_engine("sqlite:///:memory:",echo=True) #create the inmemory sqlite database reference to connect, echo to log the sql statements which is better for learning

Base = declarative_base() #metadata of the table automaically created by the declarative base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nick_name = Column(String) 
    full_name = Column(String)

    def __repr__(self):
        return "<User(name=%s, full_name=%s, nick_name=%s)>" % (self.name, self.full_name, self.nick_name)

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

user = User(name="foo",full_name="foo bar", nick_name = "foo bar nick name")
session.add(user) #add the user

#At this point, we say that the instance is pending; no SQL has yet been issued and the object is not yet represented by a row in the database. The Session will issue the SQL to persist foo bar as soon as is needed, using a process known as a flush. If we query the database for foo bar, all pending information will first be flushed, and the query is issued immediately thereafter.
#select statement for the foo named user

foo_user = session.query(User).filter_by(name="foo").first()

#now you see foo_user and user we inserted are the same

print("%s is %s: %s"%(user,foo_user,user is foo_user))

#bulk insert

session.add([
User(name="foo 2", full_name = "foo bar 2",nick_name = "foo bar nick name 2")

User(name="foo 3", full_name = "foo bar 3",nick_name = "foo bar nick name 3")

User(name="foo 4", full_name = "foo bar 4",nick_name = "foo bar nick name 4")
])

#update the user we previously created
user.name = "modified foo 1 name"

#to check for the pending transactions for new and modified changes to the database in the session
print("new objects to create:")
print(session.new)

print("modified objects:")
print(session.dirty)

#to force committing all the changes to the database
session.commit() #this will update the database with all the changes in the session
