
def _literal_float(s):
    """return True if s is space-trimmed number literal else False

    Python allows underscore as digit separators: there must be a
    digit on each side. So neither a leading underscore nor a
    double underscore are valid as part of a number. A number does
    not have to precede the decimal point, but there must be a
    digit before the optional "e" or "E" that begins the signs
    exponent of the number which must be an integer, perhaps with
    underscore separators.

    SymPy allows space as a separator; if the calling routine replaces
    them with underscores then the same semantics will be enforced
    for them as for underscores: there can only be 1 *between* digits.

    We don't check for error from float(s) because we don't know
    whether s is malicious or not. A regex for this could maybe
    be written but will it be understood by most who read it?
    """
    # mantissa and exponent
    parts = s.split('e')
    if len(parts) > 2:
        return False
    if len(parts) == 2:
        m, e = parts
        if e.startswith(tuple('+-')):
            e = e[1:]
        if not e:
            return False
    else:
        m, e = s, '1'
    # integer and fraction of mantissa
    parts = m.split('.')
    if len(parts) > 2:
        return False
    elif len(parts) == 2:
        i, f = parts
    else:
        i, f = m, '1'
    if not i and not f:
        return False
    if i and i[0] in '+-':
        i = i[1:]
    if not i:  # -.3e4 -> -0.3e4
        i = '1'
    f = f or '1'
    # check that all groups contain only digits and are not null
    for n in (i, f, e):
        for g in n.split('_'):
            if not g or g.translate(_dig):
                return False
    return True

