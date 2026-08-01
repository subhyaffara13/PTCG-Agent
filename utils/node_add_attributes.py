
def NodeAddAttributes(builder, attributes):
    builder.PrependUOffsetTRelativeSlot(10, flatbuffers.number_types.UOffsetTFlags.py_type(attributes), 0)

