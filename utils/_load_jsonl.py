import json
import os
from typing import List

def _load_jsonl(filename: str) -> List[dict]:
    """Load eval cases from a JSONL file. One JSON object per line."""
    cases = []
    path = os.path.join(EVAL_DIR, filename)
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cases.append(
                {
                    "sentence": obj["sentence"],
                    "expected": obj["expected"],
                    "test": obj["test"],
                }
            )
    return cases

