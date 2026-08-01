
def ModelAddOpsetImport(builder, opsetImport):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(opsetImport), 0)

