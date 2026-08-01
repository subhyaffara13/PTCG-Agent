
def _deserialize_json_dict(data: Any) -> Optional[Dict[str, str]]:
    """
    Deserialize optional JSON mappings stored in the database.

    Accepts values kept as JSON strings or materialized dictionaries and
    returns None when the input is empty or cannot be decoded.
    """
    if not data:
        return None

    if isinstance(data, str):
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON, return as-is (shouldn't happen but safety)
            return None
    else:
        # Already a dictionary
        return data

