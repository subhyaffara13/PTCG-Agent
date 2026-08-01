
def NodeAddExecutionProviderType(builder, executionProviderType):
    builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(executionProviderType), 0)

