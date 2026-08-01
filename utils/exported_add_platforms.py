
def ExportedAddPlatforms(builder, platforms):
    builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(platforms), 0)

