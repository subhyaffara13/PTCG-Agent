
def ExportedAddModuleKeptVarIdx(builder, moduleKeptVarIdx):
    builder.PrependUOffsetTRelativeSlot(15, flatbuffers.number_types.UOffsetTFlags.py_type(moduleKeptVarIdx), 0)

