
def _print_as_set(s) -> str:
    arg = ", ".join([pprint_thing(el) for el in s])
    return f"{{{arg}}}"

