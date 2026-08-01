
def PyTreeDefAddCustomName(builder, customName):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(customName), 0)

