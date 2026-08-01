
def sortedTagList(
    tagList: Sequence[str], tableOrder: Sequence[str] | None = None
) -> list[str]:
    """Return a sorted copy of tagList, sorted according to the OpenType
    specification, or according to a custom tableOrder. If given and not
    None, tableOrder needs to be a list of tag names.
    """
    tagList = sorted(tagList)
    if tableOrder is None:
        if "DSIG" in tagList:
            # DSIG should be last (XXX spec reference?)
            tagList.remove("DSIG")
            tagList.append("DSIG")
        if "CFF " in tagList:
            tableOrder = OTFTableOrder
        else:
            tableOrder = TTFTableOrder
    orderedTables = []
    for tag in tableOrder:
        if tag in tagList:
            orderedTables.append(tag)
            tagList.remove(tag)
    orderedTables.extend(tagList)
    return orderedTables

