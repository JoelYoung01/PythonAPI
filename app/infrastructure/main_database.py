"""The main_database module is used to create the main database engine and session."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load env variables (this is the first place in the code that needs them)
load_dotenv()

# Fetch connection string from env variables
CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "")
DATABASE = "main"

engine = create_engine(f"{CONNECTION_STRING}/{DATABASE}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
