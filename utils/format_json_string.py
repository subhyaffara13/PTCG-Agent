
def format_json_string(s: str) -> str:
    """Attempts to pretty-print a JSON string or a markdown-fenced JSON string."""
    if not s:
        return s

    # Try to extract from markdown fences
    if "```json" in s:
        start = s.find("```json") + 7
        end = s.find("```", start)
        s = s[start:end].strip()
    elif "```" in s:
        start = s.find("```") + 3
        end = s.find("```", start)
        s = s[start:end].strip()

    try:
        data = json.loads(s)
        return json.dumps(data, indent=2)
    except:
        return s


def format_json_string(s: str) -> str:
    """Attempts to pretty-print a JSON string or a markdown-fenced JSON string."""
    if not s:
        return s
    if "```json" in s:
        start = s.find("```json") + 7
        end = s.find("```", start)
        s = s[start:end].strip()
    elif "```" in s:
        start = s.find("```") + 3
        end = s.find("```", start)
        s = s[start:end].strip()
    try:
        data = json.loads(s)
        return json.dumps(data, indent=2)
    except:
        return s

