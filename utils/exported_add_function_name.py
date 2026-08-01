
def ExportedAddFunctionName(builder, functionName):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(functionName), 0)

