
def TypeInfoAddValueType(builder, valueType):
    builder.PrependUint8Slot(1, valueType, 0)

