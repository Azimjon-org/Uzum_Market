from os import getenv

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f"postgresql+psycopg2://{getenv('DB_USER')}:{getenv('PASSWORD')}@{getenv('HOST')}/{getenv('DB_NAME')}",
                       echo=False)
