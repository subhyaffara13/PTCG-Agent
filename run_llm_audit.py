import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

# Initialize the OpenAI client.
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

from utils.get_codebase_files import get_codebase_files

from utils.read_files_in_batches import read_files_in_batches

from utils.agent_1_architect import agent_1_architect

from utils.agent_2_resilience import agent_2_resilience

from utils.main import main

if __name__ == "__main__":
    main()
