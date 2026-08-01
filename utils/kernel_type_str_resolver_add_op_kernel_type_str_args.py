
def KernelTypeStrResolverAddOpKernelTypeStrArgs(builder, opKernelTypeStrArgs):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(opKernelTypeStrArgs), 0)

