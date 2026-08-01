
def NodeEdgeAddInputEdges(builder, inputEdges):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(inputEdges), 0)

