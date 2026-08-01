
def interpolate_cff2_PrivateDict(topDict, interpolateFromDeltas):
    pd_blend_lists = (
        "BlueValues",
        "OtherBlues",
        "FamilyBlues",
        "FamilyOtherBlues",
        "StemSnapH",
        "StemSnapV",
    )
    pd_blend_values = ("BlueScale", "BlueShift", "BlueFuzz", "StdHW", "StdVW")
    for fontDict in topDict.FDArray:
        pd = fontDict.Private
        vsindex = pd.vsindex if (hasattr(pd, "vsindex")) else 0
        for key, value in pd.rawDict.items():
            if (key in pd_blend_values) and isinstance(value, list):
                delta = interpolateFromDeltas(vsindex, value[1:])
                pd.rawDict[key] = otRound(value[0] + delta)
            elif (key in pd_blend_lists) and isinstance(value[0], list):
                """If any argument in a BlueValues list is a blend list,
                then they all are. The first value of each list is an
                absolute value. The delta tuples are calculated from
                relative master values, hence we need to append all the
                deltas to date to each successive absolute value."""
                delta = 0
                for i, val_list in enumerate(value):
                    delta += otRound(interpolateFromDeltas(vsindex, val_list[1:]))
                    value[i] = val_list[0] + delta

