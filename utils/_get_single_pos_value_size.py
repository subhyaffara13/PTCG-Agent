
def _getSinglePosValueSize(valueKey):
    # Returns how many ushorts this valueKey (short form of ValueRecord) takes up
    count = 0
    for _, v in valueKey[1:]:
        if isinstance(v, _DeviceTuple):
            count += len(v.DeltaValue) + 3
        else:
            count += 1
    return count

