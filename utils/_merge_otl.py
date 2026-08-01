
def _merge_OTL(font, model, master_fonts, axisTags):
    otl_tags = ["GSUB", "GDEF", "GPOS"]
    if not any(tag in font for tag in otl_tags):
        return

    log.info("Merging OpenType Layout tables")
    merger = VariationMerger(model, axisTags, font)

    merger.mergeTables(font, master_fonts, otl_tags)
    store = merger.store_builder.finish()
    if not store:
        return
    try:
        GDEF = font["GDEF"].table
        assert GDEF.Version <= 0x00010002
    except KeyError:
        GDEFTable = font["GDEF"] = newTable("GDEF")
        GDEF = GDEFTable.table = ot.GDEF()
        GDEF.GlyphClassDef = None
        GDEF.AttachList = None
        GDEF.LigCaretList = None
        GDEF.MarkAttachClassDef = None
        GDEF.MarkGlyphSetsDef = None

    GDEF.Version = 0x00010003
    GDEF.VarStore = store

    # Optimize
    varidx_map = store.optimize()
    GDEF.remap_device_varidxes(varidx_map)
    if "GPOS" in font:
        font["GPOS"].table.remap_device_varidxes(varidx_map)

