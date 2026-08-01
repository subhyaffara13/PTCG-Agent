
def InferenceSessionAddKernelTypeStrResolver(builder, kernelTypeStrResolver):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(kernelTypeStrResolver), 0)

