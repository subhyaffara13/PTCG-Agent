
def TypeInfoAddDenotation(builder, denotation):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(denotation), 0)

