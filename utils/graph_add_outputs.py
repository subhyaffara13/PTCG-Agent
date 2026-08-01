
def GraphAddOutputs(builder, outputs):
    builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(outputs), 0)

