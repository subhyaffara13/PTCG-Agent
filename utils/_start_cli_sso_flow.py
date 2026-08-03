from typing import Any, Dict

def _start_cli_sso_flow(base_url: str) -> Dict[str, Any]:
    response = requests.post(f"{base_url}/sso/cli/start", timeout=10)
    response.raise_for_status()
    data = response.json()
    required_fields = ("login_id", "poll_secret", "user_code")
    if not all(isinstance(data.get(field), str) for field in required_fields):
        raise ValueError("Invalid CLI SSO start response")
    return data

