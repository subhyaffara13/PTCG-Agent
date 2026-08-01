
def NodesToOptimizeIndicesAddNodeIndices(builder, nodeIndices):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(nodeIndices), 0)

