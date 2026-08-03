import re
from typing import List

def _find_mentioned_players(text: str, all_player_ids: List[PlayerID]) -> List[PlayerID]:
    """
    Finds player IDs mentioned in a string of text, ordered by their first appearance.
    Player IDs are treated as whole words.
    Example: "I think gpt-4 is suspicious, what do you think John?" -> ["gpt-4", "John"]
    """
    if not text or not all_player_ids:
        return []

    # Sort by length descending to handle substrings correctly.
    sorted_player_ids = sorted(all_player_ids, key=len, reverse=True)
    pattern = r"\b(" + "|".join(re.escape(pid) for pid in sorted_player_ids) + r")\b"

    matches = re.finditer(pattern, text)

    # Deduplicate while preserving order of first appearance
    ordered_mentioned_ids = []
    seen = set()
    for match in matches:
        player_id = match.group(1)
        if player_id not in seen:
            ordered_mentioned_ids.append(player_id)
            seen.add(player_id)

    return ordered_mentioned_ids

