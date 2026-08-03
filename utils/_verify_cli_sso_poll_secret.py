from typing import Optional

def _verify_cli_sso_poll_secret(flow: dict, poll_secret: Optional[str]) -> bool:
    expected_poll_secret_hash = flow.get("poll_secret_hash")
    if not isinstance(expected_poll_secret_hash, str) or not isinstance(
        poll_secret, str
    ):
        return False
    supplied_poll_secret_hash = _hash_cli_sso_secret(poll_secret)
    return secrets.compare_digest(supplied_poll_secret_hash, expected_poll_secret_hash)

