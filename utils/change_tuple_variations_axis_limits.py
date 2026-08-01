
def changeTupleVariationsAxisLimits(variations, axisLimits):
    for axisTag, axisLimit in sorted(axisLimits.items()):
        newVariations = []
        for var in variations:
            newVariations.extend(changeTupleVariationAxisLimit(var, axisTag, axisLimit))
        variations = newVariations
    return variations

