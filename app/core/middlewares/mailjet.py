from dotenv import load_dotenv
import os
from mailjet_rest import Client

load_dotenv()

MAILJET_API_KEY = os.environ.get("MAILJET_API_KEY")
MAILJET_SECRET = os.environ.get("MAILJET_SECRET")

client = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET), version="v3.1")
