
def OpIdKernelTypeStrArgsEntryAddOpId(builder, opId):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(opId), 0)

