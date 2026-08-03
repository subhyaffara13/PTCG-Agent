from typing import Any, Optional

def _snippet_str(text: Any, max_len: int = 200) -> Optional[str]:
    if text is None:
        return None
    if isinstance(text, str):
        s = text
    elif isinstance(text, list):
        parts = []
        for item in text:
            if isinstance(item, dict) and "content" in item:
                c = item["content"]
                parts.append(c if isinstance(c, str) else str(c))
            else:
                parts.append(str(item))
        s = " ".join(parts)
    else:
        s = str(text)
    if not s or s == "{}":
        return None
    return (s[:max_len] + "...") if len(s) > max_len else s

