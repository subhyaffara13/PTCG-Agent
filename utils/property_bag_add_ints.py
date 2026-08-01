
def PropertyBagAddInts(builder, ints):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(ints), 0)

