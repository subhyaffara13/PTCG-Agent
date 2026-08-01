
def AttributeAddGraphs(builder, graphs):
    builder.PrependUOffsetTRelativeSlot(12, flatbuffers.number_types.UOffsetTFlags.py_type(graphs), 0)

