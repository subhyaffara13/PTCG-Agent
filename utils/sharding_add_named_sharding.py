
def ShardingAddNamedSharding(builder, namedSharding):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(namedSharding), 0)

