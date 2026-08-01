
def PyTreeDefAddChildrenNames(builder, childrenNames):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(childrenNames), 0)

