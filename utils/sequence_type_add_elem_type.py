
def SequenceTypeAddElemType(builder, elemType):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(elemType), 0)

