
def ExportedAddDisabledChecks(builder, disabledChecks):
    builder.PrependUOffsetTRelativeSlot(12, flatbuffers.number_types.UOffsetTFlags.py_type(disabledChecks), 0)

