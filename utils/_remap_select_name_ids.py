
def _remap_select_name_ids(font: ttLib.TTFont, needRemapping: set[int]) -> None:
    """Remap a set of IDs so that the originals can be safely scrambled or
    dropped.

    For each name record whose name id is in the `needRemapping` set, make a copy
    and allocate a new unused name id in the font-specific range (> 255).

    Finally update references to these in the `fvar` and `STAT` tables.
    """

    if "fvar" not in font and "STAT" not in font:
        return

    name = font["name"]

    # 1. Assign new IDs for names to be preserved.
    existingIds = {record.nameID for record in name.names}
    remapping = {}
    nextId = name._findUnusedNameID() - 1  # Should skip gaps in name IDs.
    for nameId in needRemapping:
        nextId += 1  # We should have complete freedom until 32767.
        assert nextId not in existingIds, "_findUnusedNameID did not skip gaps"
        if nextId > 32767:
            raise ValueError("Ran out of name IDs while trying to remap existing ones.")
        remapping[nameId] = nextId

    # 2. Copy records to use the new ID. We can't rewrite them in place, because
    #    that could make IDs 1 to 6 "disappear" from code that follows. Some
    #    tools that produce EOT fonts expect them to exist, even when they're
    #    scrambled. See https://github.com/fonttools/fonttools/issues/165.
    copiedRecords = []
    for record in name.names:
        if record.nameID not in needRemapping:
            continue
        recordCopy = makeName(
            record.string,
            remapping[record.nameID],
            record.platformID,
            record.platEncID,
            record.langID,
        )
        copiedRecords.append(recordCopy)
    name.names.extend(copiedRecords)

    # 3. Rewrite the corresponding IDs in other tables. For now, care only about
    #    STAT and fvar. If more tables need to be changed, consider adapting
    #    NameRecordVisitor to rewrite IDs wherever it finds them.
    fvar = font.get("fvar")
    if fvar is not None:
        for axis in fvar.axes:
            axis.axisNameID = remapping.get(axis.axisNameID, axis.axisNameID)
        for instance in fvar.instances:
            nameID = instance.subfamilyNameID
            instance.subfamilyNameID = remapping.get(nameID, nameID)
            nameID = instance.postscriptNameID
            instance.postscriptNameID = remapping.get(nameID, nameID)

    stat = font.get("STAT")
    if stat is None:
        return
    elidedNameID = stat.table.ElidedFallbackNameID
    stat.table.ElidedFallbackNameID = remapping.get(elidedNameID, elidedNameID)
    if stat.table.DesignAxisRecord:
        for axis in stat.table.DesignAxisRecord.Axis:
            axis.AxisNameID = remapping.get(axis.AxisNameID, axis.AxisNameID)
    if stat.table.AxisValueArray:
        for value in stat.table.AxisValueArray.AxisValue:
            value.ValueNameID = remapping.get(value.ValueNameID, value.ValueNameID)

