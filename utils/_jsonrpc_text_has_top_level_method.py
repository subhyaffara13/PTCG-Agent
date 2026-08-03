from typing import List

def _jsonrpc_text_has_top_level_method(text: str) -> bool:
    """Whether a (possibly truncated) JSON-RPC envelope has a ``method`` key at
    the root object's top level.

    Used to tell a request/notification (carries ``method``) apart from a
    response (carries ``result``/``error`` and no top-level ``method``). A
    response payload can itself nest a ``method`` field, so only keys at the
    root object's depth are inspected rather than searching the whole string.
    Returns ``True`` only when a top-level ``method`` key is positively found;
    truncation that hides it yields ``False``.
    """
    depth = 0
    in_string = False
    escaped = False
    in_object: List[bool] = []
    reading_key = False
    expect_key = False
    key_chars: List[str] = []
    for ch in text:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
                if reading_key and depth == 1 and "".join(key_chars) == "method":
                    return True
            elif reading_key:
                key_chars.append(ch)
            continue
        if ch == '"':
            in_string = True
            reading_key = expect_key and depth >= 1 and in_object[-1]
            key_chars = []
            expect_key = False
        elif ch == "{" or ch == "[":
            depth += 1
            in_object.append(ch == "{")
            expect_key = ch == "{"
        elif ch == "}" or ch == "]":
            if in_object:
                in_object.pop()
            depth -= 1
            if depth <= 0:
                break
            expect_key = False
        elif ch == ",":
            expect_key = bool(in_object) and in_object[-1]
        elif ch == ":":
            expect_key = False
    return False

