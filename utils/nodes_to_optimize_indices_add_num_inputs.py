
def NodesToOptimizeIndicesAddNumInputs(builder, numInputs):
    builder.PrependUint32Slot(1, numInputs, 0)

