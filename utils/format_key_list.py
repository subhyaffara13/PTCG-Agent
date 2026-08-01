
def format_key_list(keys: list[str], *, short: bool = False) -> str:
    formatted_keys = [f'"{key}"' for key in keys]
    td = "" if short else "TypedDict "
    if len(keys) == 0:
        return f"no {td}keys"
    elif len(keys) == 1:
        return f"{td}key {formatted_keys[0]}"
    else:
        return f"{td}keys ({', '.join(formatted_keys)})"

