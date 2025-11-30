import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FDA Food Adverse Event AI Agent"
    VERSION: str = "0.2.0"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    FDA_API_URL: str = "https://api.fda.gov/food/event.json"

settings = Settings()
