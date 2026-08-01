
def _add_MVAR(font, masterModel, master_ttfs, axisTags):
    log.info("Generating MVAR")

    store_builder = varStore.OnlineVarStoreBuilder(axisTags)

    records = []
    lastTableTag = None
    fontTable = None
    tables = None
    # HACK: we need to special-case post.underlineThickness and .underlinePosition
    # and unilaterally/arbitrarily define a sentinel value to distinguish the case
    # when a post table is present in a given master simply because that's where
    # the glyph names in TrueType must be stored, but the underline values are not
    # meant to be used for building MVAR's deltas. The value of -0x8000 (-32768)
    # the minimum FWord (int16) value, was chosen for its unlikelyhood to appear
    # in real-world underline position/thickness values.
    specialTags = {"unds": -0x8000, "undo": -0x8000}

    for tag, (tableTag, itemName) in sorted(MVAR_ENTRIES.items(), key=lambda kv: kv[1]):
        # For each tag, fetch the associated table from all fonts (or not when we are
        # still looking at a tag from the same tables) and set up the variation model
        # for them.
        if tableTag != lastTableTag:
            tables = fontTable = None
            if tableTag in font:
                fontTable = font[tableTag]
                tables = []
                for master in master_ttfs:
                    if tableTag not in master or (
                        tag in specialTags
                        and getattr(master[tableTag], itemName) == specialTags[tag]
                    ):
                        tables.append(None)
                    else:
                        tables.append(master[tableTag])
                model, tables = masterModel.getSubModel(tables)
                store_builder.setModel(model)
            lastTableTag = tableTag

        if tables is None:  # Tag not applicable to the master font.
            continue

        # TODO support gasp entries

        master_values = [getattr(table, itemName) for table in tables]
        if models.allEqual(master_values):
            base, varIdx = master_values[0], None
        else:
            base, varIdx = store_builder.storeMasters(master_values)
        setattr(fontTable, itemName, base)

        if varIdx is None:
            continue
        log.info("	%s: %s.%s	%s", tag, tableTag, itemName, master_values)
        rec = ot.MetricsValueRecord()
        rec.ValueTag = tag
        rec.VarIdx = varIdx
        records.append(rec)

    assert "MVAR" not in font
    if records:
        store = store_builder.finish()
        # Optimize
        mapping = store.optimize()
        for rec in records:
            rec.VarIdx = mapping[rec.VarIdx]

        MVAR = font["MVAR"] = newTable("MVAR")
        mvar = MVAR.table = ot.MVAR()
        mvar.Version = 0x00010000
        mvar.Reserved = 0
        mvar.VarStore = store
        # XXX these should not be hard-coded but computed automatically
        mvar.ValueRecordSize = 8
        mvar.ValueRecordCount = len(records)
        mvar.ValueRecord = sorted(records, key=lambda r: r.ValueTag)

