
def DeprecatedNodeIndexAndKernelDefHashAddKernelDefHash(builder, kernelDefHash):
    builder.PrependUint64Slot(1, kernelDefHash, 0)

