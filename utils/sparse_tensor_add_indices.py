
def SparseTensorAddIndices(builder, indices):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(indices), 0)

