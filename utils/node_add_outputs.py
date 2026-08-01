
def NodeAddOutputs(builder, outputs):
    builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(outputs), 0)

