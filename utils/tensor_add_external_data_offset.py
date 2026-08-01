
def TensorAddExternalDataOffset(builder, externalDataOffset):
    builder.PrependInt64Slot(6, externalDataOffset, -1)

