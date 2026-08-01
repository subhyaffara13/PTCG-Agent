
def ModuleStateAddRequiresGradParams(builder, requiresGradParams):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(requiresGradParams), 0)

