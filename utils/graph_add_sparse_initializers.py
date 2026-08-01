
def GraphAddSparseInitializers(builder, sparseInitializers):
    builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(sparseInitializers), 0)

