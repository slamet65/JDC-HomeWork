from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

URL_DATABASE = os.getenv("DB_URL")

engine = create_engine(URL_DATABASE, pool_size= 10, max_overflow= 30)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()