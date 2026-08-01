
def ModuleStateAddFrozenParams(builder, frozenParams):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(frozenParams), 0)

