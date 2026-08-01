
def _pruneGDEF(font):
    if "GDEF" not in font:
        return
    gdef = font["GDEF"]
    table = gdef.table
    if not hasattr(table, "VarStore"):
        return

    store = table.VarStore

    usedVarIdxes = set()

    # Collect.
    table.collect_device_varidxes(usedVarIdxes)
    if "GPOS" in font:
        font["GPOS"].table.collect_device_varidxes(usedVarIdxes)

    # Subset.
    varidx_map = store.subset_varidxes(usedVarIdxes)

    # Map.
    table.remap_device_varidxes(varidx_map)
    if "GPOS" in font:
        font["GPOS"].table.remap_device_varidxes(varidx_map)

