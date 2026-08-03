import copy
from typing import Any, List, Union

def redact_nested_match_and_regex_keys(
    payload: Union[dict, List[Any], str, None],
) -> Union[dict, List[Any], str, None]:
    """
    Deep-copy `payload` and replace every `match` / `regex` string field with
    "[REDACTED]" anywhere in nested dict/list structures.

    Used for guardrail spend/compliance logging so raw spans are not persisted.
    """
    if payload is None or isinstance(payload, str):
        return payload
    try:
        redacted: Union[dict, List[Any], str, None] = copy.deepcopy(payload)
    except Exception:
        return payload

    # Iterative traversal; `seen` guards against cyclic refs preserved by deepcopy.
    try:
        seen: set = set()
        stack: List[Any] = [redacted]
        while stack:
            node = stack.pop()
            node_id = id(node)
            if node_id in seen:
                continue
            seen.add(node_id)
            if isinstance(node, dict):
                if "match" in node:
                    node["match"] = "[REDACTED]"
                if "regex" in node:
                    node["regex"] = "[REDACTED]"
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    except Exception:
        return payload
    return redacted

