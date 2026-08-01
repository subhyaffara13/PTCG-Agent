
def ExportedAddOrderedEffects(builder, orderedEffects):
    builder.PrependUOffsetTRelativeSlot(10, flatbuffers.number_types.UOffsetTFlags.py_type(orderedEffects), 0)

