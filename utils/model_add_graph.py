
def ModelAddGraph(builder, graph):
    builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(graph), 0)

