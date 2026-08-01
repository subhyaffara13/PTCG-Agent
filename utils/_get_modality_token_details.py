
def _get_modality_token_details(usage_metadata: dict, *details_keys: str) -> list:
    for details_key in details_keys:
        details = usage_metadata.get(details_key)
        if isinstance(details, list):
            return details
    return []

