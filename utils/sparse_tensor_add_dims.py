
def SparseTensorAddDims(builder, dims):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(dims), 0)

