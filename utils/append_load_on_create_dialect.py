
def append_load_on_create_dialect(dialect: str):
    global _load_on_create_dialects
    if _load_on_create_dialects is None:
        _load_on_create_dialects = [dialect]
    else:
        _load_on_create_dialects.append(dialect)

