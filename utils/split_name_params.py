
def split_name_params(schema: str) -> tuple[str, list[str]]:
    m = re.match(r"(\w+)(\.\w+)?\((.*)\)", schema)
    if m is None:
        raise RuntimeError(f"Unsupported function schema: {schema}")
    name, _, params = m.groups()
    return name, params.split(", ")

