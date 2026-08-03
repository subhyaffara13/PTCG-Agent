import json
import os
from typing import Dict

def _load_patterns_from_json() -> Dict:
    """Load pattern definitions from patterns.json file"""
    json_path = os.path.join(os.path.dirname(__file__), "patterns.json")
    with open(json_path, "r") as f:
        return json.load(f)

