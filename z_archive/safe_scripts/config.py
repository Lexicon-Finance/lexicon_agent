import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ethereum settings
RPC_URL = os.getenv("RPC_URL")
OWNER_A_PRIVATE_KEY = os.getenv("OWNER_A_PRIVATE_KEY")
