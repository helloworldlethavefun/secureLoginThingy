from sqlalchemy import *

engine = create_engine('sqlite:///users.db')

metadata = MetaData()

User = Table('User', metadata,
           Column('Id', Integer(),primary_key=True),
           Column('Email', String(255), nullable=False),
           Column('Password', String(255), nullable=False)
            )

metadata.create_all(engine)

def adduser(email):
    query = insert(User).values(Id=1, Email=email, Password='password123')
    Result = engine.execute(query)