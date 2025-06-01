import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for the application

# OpenAI API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# MySQL database configuration
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DB")