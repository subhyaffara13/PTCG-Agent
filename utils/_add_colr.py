
def _add_COLR(font, model, master_fonts, axisTags, colr_layer_reuse=True):
    merger = COLRVariationMerger(
        model, axisTags, font, allowLayerReuse=colr_layer_reuse
    )
    merger.mergeTables(font, master_fonts)
    store = merger.store_builder.finish()

    colr = font["COLR"].table
    if store:
        mapping = store.optimize()
        colr.VarStore = store
        varIdxes = [mapping[v] for v in merger.varIdxes]
        colr.VarIndexMap = builder.buildDeltaSetIndexMap(varIdxes)

