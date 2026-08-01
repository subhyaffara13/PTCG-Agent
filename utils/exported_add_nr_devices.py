
def ExportedAddNrDevices(builder, nrDevices):
    builder.PrependUint32Slot(18, nrDevices, 0)

