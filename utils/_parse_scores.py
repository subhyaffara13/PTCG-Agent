import re

def _parse_scores(observation: str) -> dict[str, int]:
    for line in observation.splitlines():
        if line.startswith("Scores"):
            # e.g. "Scores, X: 3, O: 1"
            x_match = re.search(r"X:\s*(\d+)", line)
            o_match = re.search(r"O:\s*(\d+)", line)
            return {
                _X: int(x_match.group(1)) if x_match else 0,
                _O: int(o_match.group(1)) if o_match else 0,
            }
    return {_X: 0, _O: 0}

