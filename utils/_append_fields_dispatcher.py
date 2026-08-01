
def _append_fields_dispatcher(base, names, data, dtypes=None,
                              fill_value=None, usemask=None, asrecarray=None):
    yield base
    yield from data

