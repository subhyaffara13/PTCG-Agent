
def TensorTypeAndShapeAddElemType(builder, elemType):
    builder.PrependInt32Slot(0, elemType, 0)

