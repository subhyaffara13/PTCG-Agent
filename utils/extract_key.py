from typing import Set

def extract_key(message: dict, fallback_index: int, used_keys: Set[str]) -> str:
    """
    Extract a human-readable key for the message.

    Looks for file path patterns in the content. Falls back to message_{index}.
    Handles duplicates by appending _2, _3, etc.
    """
    content = message.get("content", "")
    if isinstance(content, list):
        content = " ".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in content
        )

    key = None
    for pattern in _FILE_PATH_PATTERNS:
        match = pattern.search(content[:2000])  # Only search the beginning
        if match:
            # Use just the filename, not full path
            path = match.group(1)
            key = path.split("/")[-1]
            break

    if key is None:
        key = f"message_{fallback_index}"

    # Handle duplicates
    base_key = key
    counter = 2
    while key in used_keys:
        key = f"{base_key}_{counter}"
        counter += 1

    used_keys.add(key)
    return key

