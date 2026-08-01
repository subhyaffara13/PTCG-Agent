
def create_group(cls, group, axis='Z'):
    if not isinstance(group, str):
        raise ValueError("`group` argument must be a string")

    permitted_axes = ['x', 'y', 'z', 'X', 'Y', 'Z']
    if axis not in permitted_axes:
        raise ValueError("`axis` must be one of " + ", ".join(permitted_axes))

    if group in ['I', 'O', 'T']:
        symbol = group
        order = 1
    elif group[:1] in ['C', 'D'] and group[1:].isdigit():
        symbol = group[:1]
        order = int(group[1:])
    else:
        raise ValueError("`group` must be one of 'I', 'O', 'T', 'Dn', 'Cn'")

    if order < 1:
        raise ValueError("Group order must be positive")

    axis = 'xyz'.index(axis.lower())
    if symbol == 'I':
        return icosahedral(cls)
    elif symbol == 'O':
        return octahedral(cls)
    elif symbol == 'T':
        return tetrahedral(cls)
    elif symbol == 'D':
        return dicyclic(cls, order, axis=axis)
    elif symbol == 'C':
        return cyclic(cls, order, axis=axis)
    else:
        assert False

