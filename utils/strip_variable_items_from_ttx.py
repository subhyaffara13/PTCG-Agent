
def stripVariableItemsFromTTX(
    string: str,
    ttLibVersion: bool = True,
    checkSumAdjustment: bool = True,
    modified: bool = True,
    created: bool = True,
    sfntVersion: bool = False,  # opt-in only
) -> str:
    """Strip stuff like ttLibVersion, checksums, timestamps, etc. from TTX dumps."""
    # ttlib changes with the fontTools version
    if ttLibVersion:
        string = re.sub(' ttLibVersion="[^"]+"', "", string)
    # sometimes (e.g. some subsetter tests) we don't care whether it's OTF or TTF
    if sfntVersion:
        string = re.sub(' sfntVersion="[^"]+"', "", string)
    # head table checksum and creation and mod date changes with each save.
    if checkSumAdjustment:
        string = re.sub('<checkSumAdjustment value="[^"]+"/>', "", string)
    if modified:
        string = re.sub('<modified value="[^"]+"/>', "", string)
    if created:
        string = re.sub('<created value="[^"]+"/>', "", string)
    return string

