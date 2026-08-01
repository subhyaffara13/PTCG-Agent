
def _can_use_numexpr(op, op_str, left_op, right_op, dtype_check) -> bool:
    """return left_op boolean if we WILL be using numexpr"""
    if op_str is not None:
        # required min elements (otherwise we are adding overhead)
        if left_op.size > _MIN_ELEMENTS:
            # check for dtype compatibility
            dtypes: set[str] = set()
            for o in [left_op, right_op]:
                # ndarray and Series Case
                if hasattr(o, "dtype"):
                    dtypes |= {o.dtype.name}

            # allowed are a superset
            if not len(dtypes) or _ALLOWED_DTYPES[dtype_check] >= dtypes:
                return True

    return False

