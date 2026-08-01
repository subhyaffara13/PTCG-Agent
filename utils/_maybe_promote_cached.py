
def _maybe_promote_cached(dtype, fill_value, fill_value_type):
    # The cached version of _maybe_promote below
    # This also use fill_value_type as (unused) argument to use this in the
    # cache lookup -> to differentiate 1 and True
    return _maybe_promote(dtype, fill_value)

