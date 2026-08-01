
def GraphAddRuntimeOptimizations(builder, runtimeOptimizations):
    builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(runtimeOptimizations), 0)

