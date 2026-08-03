import re

def text_for_entity_matching(text: str) -> str:
    """Letters-only variant for entity matching (e.g. split punctuation)."""
    t = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", t).strip()

