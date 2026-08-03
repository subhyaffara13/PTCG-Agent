from typing import Any

def _estimate_json_bytes(obj: Any) -> int:
    """Estimate the JSON-serialised byte size of ``obj`` without materialising
    JSON. Walks iteratively (no recursion stack risk).

    String length is read via ``len()`` (O(1) on Python ``str``) so a target
    containing a 100MB description costs ~one walk step, not a 100MB
    serialisation. Escape sequences are not counted exactly, so this is an
    approximation -- but always within a small constant factor of the real
    serialised size, which is what a schema-bomb budget needs.
    """
    total = 0
    stack: list = [obj]
    while stack:
        x = stack.pop()
        if isinstance(x, dict):
            total += 2  # `{}`
            for k, v in x.items():
                total += len(str(k)) + 4  # `"k":,`
                stack.append(v)
        elif isinstance(x, list):
            total += 2  # `[]`
            total += max(0, len(x) - 1)  # commas between items
            stack.extend(x)
        elif isinstance(x, str):
            total += len(x) + 2
        elif isinstance(x, bool):  # bool subclasses int -- check first
            total += 4 if x else 5
        elif x is None:
            total += 4
        elif isinstance(x, (int, float)):
            total += 24  # generous upper bound for stringified numbers
        else:
            total += 24
    return total

