
def ModelAddDocString(builder, docString):
    builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(docString), 0)

