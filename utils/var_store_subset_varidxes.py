
def VarStore_subset_varidxes(
    self,
    varIdxes,
    optimize=True,
    retainFirstMap=False,
    advIdxes=set(),
    *,
    VarData="VarData",
):
    # Sort out used varIdxes by major/minor.
    used = defaultdict(set)
    for varIdx in varIdxes:
        if varIdx == NO_VARIATION_INDEX:
            continue
        major = varIdx >> 16
        minor = varIdx & 0xFFFF
        used[major].add(minor)
    del varIdxes

    #
    # Subset VarData
    #

    varData = getattr(self, VarData)
    newVarData = []
    varDataMap = {NO_VARIATION_INDEX: NO_VARIATION_INDEX}
    for major, data in enumerate(varData):
        usedMinors = used.get(major)
        if usedMinors is None:
            continue
        newMajor = len(newVarData)
        newVarData.append(data)

        items = data.Item
        newItems = []
        if major == 0 and retainFirstMap:
            for minor in range(len(items)):
                newItems.append(
                    items[minor] if minor in usedMinors else [0] * len(items[minor])
                )
                varDataMap[minor] = minor
        else:
            if major == 0:
                minors = sorted(advIdxes) + sorted(usedMinors - advIdxes)
            else:
                minors = sorted(usedMinors)
            for minor in minors:
                newMinor = len(newItems)
                newItems.append(items[minor])
                varDataMap[(major << 16) + minor] = (newMajor << 16) + newMinor

        data.Item = newItems
        data.ItemCount = len(data.Item)

        if VarData == "VarData":
            data.calculateNumShorts(optimize=optimize)

    setattr(self, VarData, newVarData)
    setattr(self, VarData + "Count", len(newVarData))

    self.prune_regions()

    return varDataMap

