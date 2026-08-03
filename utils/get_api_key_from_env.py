from typing import Optional

def get_api_key_from_env() -> Optional[str]:
    return get_secret_str("GOOGLE_API_KEY") or get_secret_str("GEMINI_API_KEY")

