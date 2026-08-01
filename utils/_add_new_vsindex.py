
def _add_new_vsindex(
    model, key, masterSupports, vsindex_dict, vsindex_by_key, varDataList
):
    varTupleIndexes = []
    for support in model.supports[1:]:
        if support not in masterSupports:
            masterSupports.append(support)
        varTupleIndexes.append(masterSupports.index(support))
    var_data = varLib.builder.buildVarData(varTupleIndexes, None, False)
    vsindex = len(vsindex_dict)
    vsindex_by_key[key] = vsindex
    vsindex_dict[vsindex] = (model, [key])
    varDataList.append(var_data)
    return vsindex

