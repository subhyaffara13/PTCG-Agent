
def PartitionSpecOneAxisAddAxes(builder, axes):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(axes), 0)

