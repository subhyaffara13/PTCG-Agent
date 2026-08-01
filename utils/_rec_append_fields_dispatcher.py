
def _rec_append_fields_dispatcher(base, names, data, dtypes=None):
    yield base
    yield from data

