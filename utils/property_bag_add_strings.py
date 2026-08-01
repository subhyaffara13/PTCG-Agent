
def PropertyBagAddStrings(builder, strings):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(strings), 0)

