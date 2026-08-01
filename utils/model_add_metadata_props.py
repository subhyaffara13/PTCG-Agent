
def ModelAddMetadataProps(builder, metadataProps):
    builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(metadataProps), 0)

