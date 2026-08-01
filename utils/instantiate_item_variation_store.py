
def instantiateItemVariationStore(
    itemVarStore, fvarAxes, axisLimits, hierarchical=False
):
    """Compute deltas at partial location, and update varStore in-place.

    Remove regions in which all axes were instanced, or fall outside the new axis
    limits. Scale the deltas of the remaining regions where only some of the axes
    were instanced.

    The number of VarData subtables, and the number of items within each, are
    not modified, in order to keep the existing VariationIndex valid.
    One may call VarStore.optimize() method after this to further optimize those.

    Args:
        varStore: An otTables.VarStore object (Item Variation Store)
        fvarAxes: list of fvar's Axis objects
        axisLimits: NormalizedAxisLimits: mapping axis tags to normalized
            min/default/max axis coordinates. May not specify coordinates/ranges for
            all the fvar axes.

    Returns:
        defaultDeltas: to be added to the default instance, of type dict of floats
            keyed by VariationIndex compound values: i.e. (outer << 16) + inner.
    """
    tupleVarStore = _TupleVarStoreAdapter.fromItemVarStore(itemVarStore, fvarAxes)
    defaultDeltaArray = tupleVarStore.instantiate(axisLimits)
    newItemVarStore = tupleVarStore.asItemVarStore()

    itemVarStore.VarRegionList = newItemVarStore.VarRegionList
    if not hasattr(itemVarStore, "VarDataCount"):  # Happens fromXML
        itemVarStore.VarDataCount = len(newItemVarStore.VarData)
    assert itemVarStore.VarDataCount == newItemVarStore.VarDataCount
    itemVarStore.VarData = newItemVarStore.VarData

    if not hierarchical:
        defaultDeltas = {
            ((major << 16) + minor): delta
            for major, deltas in enumerate(defaultDeltaArray)
            for minor, delta in enumerate(deltas)
        }
        defaultDeltas[itemVarStore.NO_VARIATION_INDEX] = 0
    else:
        defaultDeltas = {0xFFFF: {0xFFFF: 0}}  # NO_VARIATION_INDEX
        for major, deltas in enumerate(defaultDeltaArray):
            defaultDeltasForMajor = defaultDeltas.setdefault(major, {})
            for minor, delta in enumerate(deltas):
                defaultDeltasForMajor[minor] = delta
    return defaultDeltas

