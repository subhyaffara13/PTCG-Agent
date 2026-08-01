
def _strip_prefix(s, prefix):
  return s[len(prefix):] if s.startswith(prefix) else s


def _strip_prefix(action_str: str) -> str:
    """Drop OpenSpiel's 'Player: <id> Action: ' wrapper from an action string."""
    return _ACTION_PREFIX_RE.sub("", action_str).strip()

