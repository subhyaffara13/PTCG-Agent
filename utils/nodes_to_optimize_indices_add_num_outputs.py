
def NodesToOptimizeIndicesAddNumOutputs(builder, numOutputs):
    builder.PrependUint32Slot(2, numOutputs, 0)

