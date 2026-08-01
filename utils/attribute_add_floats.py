
def AttributeAddFloats(builder, floats):
    builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(floats), 0)

