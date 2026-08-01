
def NodesToOptimizeIndicesAddNumVariadicOutputs(builder, numVariadicOutputs):
    builder.PrependUint32Slot(6, numVariadicOutputs, 0)

