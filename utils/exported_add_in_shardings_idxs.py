
def ExportedAddInShardingsIdxs(builder, inShardingsIdxs):
    builder.PrependUOffsetTRelativeSlot(24, flatbuffers.number_types.UOffsetTFlags.py_type(inShardingsIdxs), 0)

