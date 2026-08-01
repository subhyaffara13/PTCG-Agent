
def instantiateFvar(varfont, axisLimits):
    # 'axisLimits' dict must contain user-space (non-normalized) coordinates

    location = axisLimits.pinnedLocation()

    fvar = varfont["fvar"]

    # drop table if we instantiate all the axes
    if set(location).issuperset(axis.axisTag for axis in fvar.axes):
        log.info("Dropping fvar table")
        del varfont["fvar"]
        return

    log.info("Instantiating fvar table")

    axes = []
    for axis in fvar.axes:
        axisTag = axis.axisTag
        if axisTag in location:
            continue
        if axisTag in axisLimits:
            triple = axisLimits[axisTag]
            if triple.default is None:
                triple = (triple.minimum, axis.defaultValue, triple.maximum)
            axis.minValue, axis.defaultValue, axis.maxValue = triple
        axes.append(axis)
    fvar.axes = axes

    # only keep NamedInstances whose coordinates == pinned axis location
    instances = []
    for instance in fvar.instances:
        if any(instance.coordinates[axis] != value for axis, value in location.items()):
            continue
        for axisTag in location:
            del instance.coordinates[axisTag]
        if not isInstanceWithinAxisRanges(instance.coordinates, axisLimits):
            continue
        instances.append(instance)
    fvar.instances = instances

