
def ExportedAddInTree(builder, inTree):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(inTree), 0)

