from typing import List, Tuple

def _parse_cli_sso_claim_map() -> List[Tuple[str, str]]:
    """
    Parse CLI_SSO_CLAIM_MAP / LITELLM_CLI_SSO_CLAIM_MAP.

    Format: comma-separated ``source_claim->metadata_key`` pairs, e.g.
    ``employment_type->acme_employment_type,org_info.department->department``.
    Destination keys may use an optional ``metadata.`` prefix; values are stored
    on the LiteLLM user's ``metadata`` JSON column.
    """
    claim_map_raw = CLI_SSO_CLAIM_MAP.strip()
    if not claim_map_raw:
        return []

    parsed: List[Tuple[str, str]] = []
    for entry in claim_map_raw.split(","):
        entry = entry.strip()
        if not entry or "->" not in entry:
            continue
        source_claim, dest_key = entry.split("->", 1)
        source_claim = source_claim.strip()
        dest_key = dest_key.strip()
        if dest_key.startswith("metadata."):
            dest_key = dest_key[len("metadata.") :]
        if source_claim and dest_key:
            parsed.append((source_claim, dest_key))
    return parsed

