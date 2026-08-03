from typing import Any, Dict

def _prepare_key_import_data(key: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare key data for import by extracting relevant fields."""
    import_data = {}

    # Copy relevant fields if they exist
    for field in [
        "models",
        "aliases",
        "spend",
        "key_alias",
        "team_id",
        "user_id",
        "budget_id",
        "config",
    ]:
        if key.get(field):
            import_data[field] = key[field]

    return import_data

