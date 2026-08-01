
def PyTreeDefAddCustomAuxdata(builder, customAuxdata):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(customAuxdata), 0)

