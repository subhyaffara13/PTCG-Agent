
def ExportedAddMlirModuleSerialized(builder, mlirModuleSerialized):
    builder.PrependUOffsetTRelativeSlot(13, flatbuffers.number_types.UOffsetTFlags.py_type(mlirModuleSerialized), 0)

