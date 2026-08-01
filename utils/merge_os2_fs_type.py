
def mergeOs2FsType(lst):
    lst = list(lst)
    if all(item == 0 for item in lst):
        return 0

    # Compute least restrictive logic for each fsType value
    for i in range(len(lst)):
        # unset bit 1 (no embedding permitted) if either bit 2 or 3 is set
        if lst[i] & 0x000C:
            lst[i] &= ~0x0002
        # set bit 2 (allow previewing) if bit 3 is set (allow editing)
        elif lst[i] & 0x0008:
            lst[i] |= 0x0004
        # set bits 2 and 3 if everything is allowed
        elif lst[i] == 0:
            lst[i] = 0x000C

    fsType = mergeBits(os2FsTypeMergeBitMap)(lst)
    # unset bits 2 and 3 if bit 1 is set (some font is "no embedding")
    if fsType & 0x0002:
        fsType &= ~0x000C
    return fsType

