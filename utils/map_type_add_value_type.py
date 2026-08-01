
def MapTypeAddValueType(builder, valueType):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(valueType), 0)

