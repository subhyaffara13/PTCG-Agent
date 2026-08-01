
def TensorTypeAndShapeAddShape(builder, shape):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(shape), 0)

