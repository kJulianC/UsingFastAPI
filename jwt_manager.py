import os
from dotenv import load_dotenv
from jwt import encode

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

def create_token (data : dict):
    encode(payload=data)