
def ExportedAddCallingConventionVersion(builder, callingConventionVersion):
    builder.PrependUint16Slot(14, callingConventionVersion, 0)

