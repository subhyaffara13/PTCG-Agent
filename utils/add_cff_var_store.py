
def addCFFVarStore(varFont, varModel, varDataList, masterSupports):
    fvarTable = varFont["fvar"]
    axisKeys = [axis.axisTag for axis in fvarTable.axes]
    varTupleList = varLib.builder.buildVarRegionList(masterSupports, axisKeys)
    varStoreCFFV = varLib.builder.buildVarStore(varTupleList, varDataList)

    topDict = varFont["CFF2"].cff.topDictIndex[0]
    topDict.VarStore = VarStoreData(otVarStore=varStoreCFFV)
    if topDict.FDArray[0].vstore is None:
        fdArray = topDict.FDArray
        for fontDict in fdArray:
            if hasattr(fontDict, "Private"):
                fontDict.Private.vstore = topDict.VarStore

