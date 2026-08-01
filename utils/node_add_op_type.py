
def NodeAddOpType(builder, opType):
    builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(opType), 0)

