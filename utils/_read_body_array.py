
def _read_body_array(cursor):
    """
    Read MatrixMarket array body
    """
    from . import _fmm_core

    vals = np.zeros(cursor.header.shape, dtype=_field_to_dtype.get(cursor.header.field))
    _fmm_core.read_body_array(cursor, vals)
    return vals

