
def GraphAddNodeEdges(builder, nodeEdges):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(nodeEdges), 0)

