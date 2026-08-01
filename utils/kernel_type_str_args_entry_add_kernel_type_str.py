
def KernelTypeStrArgsEntryAddKernelTypeStr(builder, kernelTypeStr):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(kernelTypeStr), 0)

