
def AttributeAddStrings(builder, strings):
    builder.PrependUOffsetTRelativeSlot(10, flatbuffers.number_types.UOffsetTFlags.py_type(strings), 0)

