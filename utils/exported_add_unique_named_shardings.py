
def ExportedAddUniqueNamedShardings(builder, uniqueNamedShardings):
    builder.PrependUOffsetTRelativeSlot(21, flatbuffers.number_types.UOffsetTFlags.py_type(uniqueNamedShardings), 0)

