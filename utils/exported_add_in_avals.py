
def ExportedAddInAvals(builder, inAvals):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(inAvals), 0)

