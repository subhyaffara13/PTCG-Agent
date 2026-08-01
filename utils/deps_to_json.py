
def deps_to_json(x: dict[str, set[str]]) -> bytes:
    return json_dumps({k: list(v) for k, v in x.items()})

