import copy
from typing import Any, Union

def _truncate_base64_in_value(value: Any) -> Any:
    """Iteratively truncate base64 data URIs in a JSON-like value (str/list/dict).

    Uses an explicit stack instead of recursion to satisfy the project's
    recursive-function detector and avoid stack-overflow on deep payloads.
    """
    # Stack entries: (source_value, depth, parent_container, key_or_index)
    # We mutate *copies* of dicts/lists in-place via parent references.
    if isinstance(value, str):
        return _truncate_base64_in_string(value)
    if not isinstance(value, (dict, list)):
        return value

    # Shallow-copy the root so we don't mutate the caller's data.
    root = {k: v for k, v in value.items()} if isinstance(value, dict) else list(value)
    stack: list = [(root, 0)]

    while stack:
        container, depth = stack.pop()
        if depth > _MAX_TRUNCATION_DEPTH:
            continue
        if isinstance(container, dict):
            for k, v in container.items():
                if isinstance(v, str):
                    container[k] = _truncate_base64_in_string(v)
                elif isinstance(v, dict):
                    copy: Union[dict, list] = {ck: cv for ck, cv in v.items()}
                    container[k] = copy
                    stack.append((copy, depth + 1))
                elif isinstance(v, list):
                    copy = list(v)
                    container[k] = copy
                    stack.append((copy, depth + 1))
        elif isinstance(container, list):
            for i, v in enumerate(container):
                if isinstance(v, str):
                    container[i] = _truncate_base64_in_string(v)
                elif isinstance(v, dict):
                    copy = {ck: cv for ck, cv in v.items()}
                    container[i] = copy
                    stack.append((copy, depth + 1))
                elif isinstance(v, list):
                    copy = list(v)
                    container[i] = copy
                    stack.append((copy, depth + 1))

    return root

