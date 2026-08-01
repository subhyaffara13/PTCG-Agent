
def short_id_from_name(func_name: str, shortname: str, line: int | None) -> str:
    if unnamed_function(func_name):
        assert line is not None
        partial_name = f"{shortname}.{line}"
    else:
        partial_name = shortname
    return partial_name

