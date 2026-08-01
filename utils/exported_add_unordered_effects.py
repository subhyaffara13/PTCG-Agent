
def ExportedAddUnorderedEffects(builder, unorderedEffects):
    builder.PrependUOffsetTRelativeSlot(11, flatbuffers.number_types.UOffsetTFlags.py_type(unorderedEffects), 0)

