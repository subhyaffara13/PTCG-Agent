
def DeprecatedKernelCreateInfosAddKernelDefHashes(builder, kernelDefHashes):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(kernelDefHashes), 0)

