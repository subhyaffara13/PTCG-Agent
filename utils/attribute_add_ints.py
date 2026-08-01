
def AttributeAddInts(builder, ints):
    builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(ints), 0)

