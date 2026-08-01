
def GraphAddNodes(builder, nodes):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(nodes), 0)

