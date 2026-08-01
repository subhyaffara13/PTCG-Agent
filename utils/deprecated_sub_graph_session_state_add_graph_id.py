
def DeprecatedSubGraphSessionStateAddGraphId(builder, graphId):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(graphId), 0)

