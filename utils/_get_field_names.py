
def _get_field_names(cls) -> set[str]:
    return {f.name for f in fields(cls)}

