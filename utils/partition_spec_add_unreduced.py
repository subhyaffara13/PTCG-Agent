
def PartitionSpecAddUnreduced(builder, unreduced):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(unreduced), 0)

