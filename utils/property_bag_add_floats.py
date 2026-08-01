
def PropertyBagAddFloats(builder, floats):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(floats), 0)

