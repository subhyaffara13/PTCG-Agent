
def ExportedAddOutAvals(builder, outAvals):
    builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(outAvals), 0)

