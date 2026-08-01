
def CheckpointAddVersion(builder, version):
    builder.PrependInt32Slot(0, version, 0)

