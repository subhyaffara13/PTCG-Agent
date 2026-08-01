
def ExportedAddOutShardingsIdxs(builder, outShardingsIdxs):
    builder.PrependUOffsetTRelativeSlot(25, flatbuffers.number_types.UOffsetTFlags.py_type(outShardingsIdxs), 0)

