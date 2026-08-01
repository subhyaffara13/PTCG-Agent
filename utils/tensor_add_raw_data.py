
def TensorAddRawData(builder, rawData):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(rawData), 0)

