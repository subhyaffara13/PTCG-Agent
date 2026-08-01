
def _is_json_parsing_error(exception) -> bool:
    out = True if isinstance(exception, pyjson5.Json5Exception) else False
    return out

