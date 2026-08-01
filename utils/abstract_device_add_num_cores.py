
def AbstractDeviceAddNumCores(builder, numCores):
    builder.PrependUint32Slot(1, numCores, None)

