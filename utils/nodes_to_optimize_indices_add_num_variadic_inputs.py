
def NodesToOptimizeIndicesAddNumVariadicInputs(builder, numVariadicInputs):
    builder.PrependUint32Slot(5, numVariadicInputs, 0)

