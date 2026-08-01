
def ExportedAddUniqueAvals(builder, uniqueAvals):
    builder.PrependUOffsetTRelativeSlot(19, flatbuffers.number_types.UOffsetTFlags.py_type(uniqueAvals), 0)

