
def ExportedAddSerializationVersion(builder, serializationVersion):
    builder.PrependUint16Slot(0, serializationVersion, 0)

