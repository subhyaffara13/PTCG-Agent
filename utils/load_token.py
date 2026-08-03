import json
import os
from typing import Any, Dict, Optional

def load_token() -> Optional[Dict[str, Any]]:
    """Load token data from file"""
    token_file = get_token_file_path()
    if not os.path.exists(token_file):
        return None

    try:
        with open(token_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

