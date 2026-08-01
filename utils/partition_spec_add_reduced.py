
def PartitionSpecAddReduced(builder, reduced):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(reduced), 0)

