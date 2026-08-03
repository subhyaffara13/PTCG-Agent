from typing import Any, Dict, Union

def _cli_poll_attribution_metadata_from_session(
    session_data: Dict[str, Any],
) -> Dict[str, Union[str, int, float, bool]]:
    stored = session_data.get("attribution_metadata")
    if isinstance(stored, dict):
        return _flatten_cli_sso_metadata_for_poll(stored)
    return {}

