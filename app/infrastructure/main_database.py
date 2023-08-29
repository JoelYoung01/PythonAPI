import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Fetch connection string from env variables
connection_string = os.environ.get("DB_CONNECTION_STRING")
database = "main"

engine = create_engine(f"{connection_string}/{database}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
