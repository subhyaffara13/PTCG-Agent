
def _group_poles(poles, tol, rtype):
    if rtype in ['max', 'maximum']:
        reduce = np.max
    elif rtype in ['min', 'minimum']:
        reduce = np.min
    elif rtype in ['avg', 'mean']:
        reduce = np.mean
    else:
        raise ValueError("`rtype` must be one of "
                         "{'max', 'maximum', 'min', 'minimum', 'avg', 'mean'}")

    unique = []
    multiplicity = []

    pole = poles[0]
    block = [pole]
    for i in range(1, len(poles)):
        if abs(poles[i] - pole) <= tol:
            block.append(pole)
        else:
            unique.append(reduce(block))
            multiplicity.append(len(block))
            pole = poles[i]
            block = [pole]

    unique.append(reduce(block))
    multiplicity.append(len(block))

    return np.asarray(unique), np.asarray(multiplicity)

