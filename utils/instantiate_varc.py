
def instantiateVARC(varfont, axisLimits):
    log.info("Instantiating VARC tables")

    # TODO(behdad) My confidence in this function is rather low;
    # It needs more testing. Specially with partial-instancing,
    # I don't think it currently works.

    varc = varfont["VARC"].table
    fvarAxes = varfont["fvar"].axes if "fvar" in varfont else []

    location = axisLimits.pinnedLocation()
    axisMap = [i for i, axis in enumerate(fvarAxes) if axis.axisTag not in location]
    reverseAxisMap = {i: j for j, i in enumerate(axisMap)}

    if varc.AxisIndicesList:
        axisIndicesList = varc.AxisIndicesList.Item
        for i, axisIndices in enumerate(axisIndicesList):
            if any(fvarAxes[j].axisTag in axisLimits for j in axisIndices):
                raise NotImplementedError(
                    "Instancing across VarComponent axes is not supported."
                )
            axisIndicesList[i] = [reverseAxisMap[j] for j in axisIndices]

    store = varc.MultiVarStore
    if store:
        for region in store.SparseVarRegionList.Region:
            newRegionAxis = []
            for regionRecord in region.SparseVarRegionAxis:
                tag = fvarAxes[regionRecord.AxisIndex].axisTag
                if tag in axisLimits:
                    raise NotImplementedError(
                        "Instancing across VarComponent axes is not supported."
                    )
                regionRecord.AxisIndex = reverseAxisMap[regionRecord.AxisIndex]

