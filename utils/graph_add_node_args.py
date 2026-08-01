
def GraphAddNodeArgs(builder, nodeArgs):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(nodeArgs), 0)

