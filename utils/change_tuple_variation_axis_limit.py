
def changeTupleVariationAxisLimit(var, axisTag, axisLimit):
    assert isinstance(axisLimit, NormalizedAxisTripleAndDistances)

    # Skip when current axis is missing or peaks at 0 (i.e. doesn't participate)
    lower, peak, upper = var.axes.get(axisTag, (-1, 0, 1))
    if peak == 0:
        # explicitly defined, no-op axes can be omitted
        # https://github.com/fonttools/fonttools/issues/3453
        if axisTag in var.axes:
            del var.axes[axisTag]
        return [var]
    # Drop if the var 'tent' isn't well-formed
    if not (lower <= peak <= upper) or (lower < 0 and upper > 0):
        return []

    if axisTag not in var.axes:
        return [var]

    tent = var.axes[axisTag]

    solutions = solver.rebaseTent(tent, axisLimit)

    out = []
    for scalar, tent in solutions:
        newVar = (
            TupleVariation(var.axes, var.coordinates) if len(solutions) > 1 else var
        )
        if tent is None:
            newVar.axes.pop(axisTag)
        else:
            assert tent[1] != 0, tent
            newVar.axes[axisTag] = tent
        newVar *= scalar
        out.append(newVar)

    return out

