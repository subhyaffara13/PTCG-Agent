
def _is_string_view(typ):
    return not pa_version_under16p0 and pa.types.is_string_view(typ)

