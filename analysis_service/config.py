import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment
TENDERLY_API_KEY = os.getenv('TENDERLY_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY')

# LLM Configuration
LLM_MODEL = "gpt-4-turbo-preview"

# Service Configuration
SERVICE_PORT = 8001
SERVICE_HOST = "0.0.0.0"

# Risk Detection Settings
MAX_TRANSACTION_AMOUNT = 10000.0
RISK_THRESHOLD = 0.8

# RPC and Contract Settings
RPC_URL = os.getenv('RPC_URL')
OWNER_A_PRIVATE_KEY = os.getenv('OWNER_A_PRIVATE_KEY')

# LangSmith Settings
LANGSMITH_TRACING = os.getenv('LANGSMITH_TRACING')
LANGSMITH_ENDPOINT = os.getenv('LANGSMITH_ENDPOINT')
LANGSMITH_PROJECT = os.getenv('LANGSMITH_PROJECT')
