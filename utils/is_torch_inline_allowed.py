
def is_torch_inline_allowed(filename: str) -> bool:
    return any(filename.startswith(d) for d in get_mod_inlinelist())

