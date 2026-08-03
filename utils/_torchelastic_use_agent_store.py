import os

def _torchelastic_use_agent_store() -> bool:
    return os.environ.get("TORCHELASTIC_USE_AGENT_STORE", None) == str(True)

