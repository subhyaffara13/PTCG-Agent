import os

def should_print_missing() -> bool:
    return os.environ.get("TORCHDYNAMO_PRINT_MISSING") == "1"

