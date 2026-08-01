
def ExportedAddInAvalsIdxs(builder, inAvalsIdxs):
    builder.PrependUOffsetTRelativeSlot(22, flatbuffers.number_types.UOffsetTFlags.py_type(inAvalsIdxs), 0)

