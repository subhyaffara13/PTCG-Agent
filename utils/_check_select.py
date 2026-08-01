
def _check_select(select, select_range, max_ev, max_len):
    """Check that select is valid, convert to Fortran style."""
    if isinstance(select, str):
        select = select.lower()
    try:
        select = _conv_dict[select]
    except KeyError as e:
        raise ValueError('invalid argument for select') from e
    vl, vu = 0., 1.
    il = iu = 1
    if select != 0:  # (non-all)
        sr = asarray(select_range)
        if sr.ndim != 1 or sr.size != 2 or sr[1] < sr[0]:
            raise ValueError('select_range must be a 2-element array-like '
                             'in nondecreasing order')
        if select == 1:  # (value)
            vl, vu = sr
            if max_ev == 0:
                max_ev = max_len
        else:  # 2 (index)
            if sr.dtype.char.lower() not in 'hilqp':
                raise ValueError(
                    f'when using select="i", select_range must '
                    f'contain integers, got dtype {sr.dtype} ({sr.dtype.char})'
                )
            # translate Python (0 ... N-1) into Fortran (1 ... N) with + 1
            il, iu = sr + 1
            if min(il, iu) < 1 or max(il, iu) > max_len:
                raise ValueError('select_range out of bounds')
            max_ev = iu - il + 1
    return select, vl, vu, il, iu, max_ev

