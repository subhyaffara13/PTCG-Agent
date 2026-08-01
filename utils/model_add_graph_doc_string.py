
def ModelAddGraphDocString(builder, graphDocString):
    builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(graphDocString), 0)

