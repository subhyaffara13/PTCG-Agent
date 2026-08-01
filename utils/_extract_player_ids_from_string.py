
def _extract_player_ids_from_string(text: str, all_player_ids: List[PlayerID]) -> List[PlayerID]:
    """Extracts player IDs mentioned in a string."""
    if not all_player_ids:
        return []
    # Create a regex pattern to find any of the player IDs as whole words
    # Using a set for faster lookups and to handle duplicates from the regex
    pattern = r"\b(" + "|".join(re.escape(pid) for pid in all_player_ids) + r")\b"
    # Use a set to automatically handle duplicates found by the regex
    found_ids = set(re.findall(pattern, text))
    return sorted(list(found_ids))  # sorted for deterministic order

