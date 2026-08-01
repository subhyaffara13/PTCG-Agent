
def DimensionAddDenotation(builder, denotation):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(denotation), 0)

