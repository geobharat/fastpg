from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(".env"))

user = os.environ.get("DB_USER")
host = os.environ.get("DB_HOST")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_NAME")
port = int(os.environ.get("DB_PORT"))
schema = os.environ.get("DB_SCHEMA")
