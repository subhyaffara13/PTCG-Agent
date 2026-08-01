
def AbstractMeshAddAxisSizes(builder, axisSizes):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(axisSizes), 0)

