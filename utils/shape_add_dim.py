
def ShapeAddDim(builder, dim):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(dim), 0)

