
def ExportedAddOutTree(builder, outTree):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(outTree), 0)

