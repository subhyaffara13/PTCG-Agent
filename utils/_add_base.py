
def _add_BASE(font, masterModel, master_ttfs, axisTags):
    log.info("Generating BASE")

    merger = VariationMerger(masterModel, axisTags, font)
    merger.mergeTables(font, master_ttfs, ["BASE"])
    store = merger.store_builder.finish()

    if not store:
        return
    base = font["BASE"].table
    assert base.Version == 0x00010000
    base.Version = 0x00010001
    base.VarStore = store

