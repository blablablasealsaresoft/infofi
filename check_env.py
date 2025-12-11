import os
from dotenv import dotenv_values

env_path = os.path.join(os.path.dirname(__file__), '.env')
config = dotenv_values(env_path)

print(f"Loaded from: {env_path}")
print(f"Keys in .env: {list(config.keys())}")
