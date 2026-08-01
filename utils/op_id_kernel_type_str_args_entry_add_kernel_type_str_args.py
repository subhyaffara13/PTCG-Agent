
def OpIdKernelTypeStrArgsEntryAddKernelTypeStrArgs(builder, kernelTypeStrArgs):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(kernelTypeStrArgs), 0)

