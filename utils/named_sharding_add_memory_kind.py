
def NamedShardingAddMemoryKind(builder, memoryKind):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(memoryKind), 0)

