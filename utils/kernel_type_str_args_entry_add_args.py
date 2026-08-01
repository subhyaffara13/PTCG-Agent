
def KernelTypeStrArgsEntryAddArgs(builder, args):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(args), 0)

