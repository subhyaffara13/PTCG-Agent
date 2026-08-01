
def ExportedAddInShardings(builder, inShardings):
    builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(inShardings), 0)

