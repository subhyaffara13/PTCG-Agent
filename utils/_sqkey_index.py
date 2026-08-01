
def _sqkey_index(index):
    """Key for sorting of indices.

    particle < hole < general

    FIXME: This is a bottle-neck, can we do it faster?
    """
    h = hash(index)
    label = str(index)
    if isinstance(index, Dummy):
        if index.assumptions0.get('above_fermi'):
            return (20, label, h)
        elif index.assumptions0.get('below_fermi'):
            return (21, label, h)
        else:
            return (22, label, h)

    if index.assumptions0.get('above_fermi'):
        return (10, label, h)
    elif index.assumptions0.get('below_fermi'):
        return (11, label, h)
    else:
        return (12, label, h)

