
def PyTreeDefAddChildren(builder, children):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(children), 0)

