
def ExportedAddOutAvalsIdxs(builder, outAvalsIdxs):
    builder.PrependUOffsetTRelativeSlot(23, flatbuffers.number_types.UOffsetTFlags.py_type(outAvalsIdxs), 0)

