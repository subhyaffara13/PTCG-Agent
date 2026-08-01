
def GraphAddInitializers(builder, initializers):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(initializers), 0)

