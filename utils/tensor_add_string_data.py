
def TensorAddStringData(builder, stringData):
    builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(stringData), 0)

