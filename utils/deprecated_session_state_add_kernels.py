
def DeprecatedSessionStateAddKernels(builder, kernels):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(kernels), 0)

