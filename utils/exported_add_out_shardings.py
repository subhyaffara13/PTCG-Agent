
def ExportedAddOutShardings(builder, outShardings):
    builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(outShardings), 0)

