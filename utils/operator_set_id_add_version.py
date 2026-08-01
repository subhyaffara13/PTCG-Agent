
def OperatorSetIdAddVersion(builder, version):
    builder.PrependInt64Slot(1, version, 0)

