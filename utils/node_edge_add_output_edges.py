
def NodeEdgeAddOutputEdges(builder, outputEdges):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(outputEdges), 0)

