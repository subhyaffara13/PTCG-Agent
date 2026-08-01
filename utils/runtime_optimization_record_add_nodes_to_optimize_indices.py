
def RuntimeOptimizationRecordAddNodesToOptimizeIndices(builder, nodesToOptimizeIndices):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(nodesToOptimizeIndices), 0)

