
def get_load_on_create_dialects():
    global _load_on_create_dialects
    if _load_on_create_dialects is None:
        _load_on_create_dialects = []
    return _load_on_create_dialects

