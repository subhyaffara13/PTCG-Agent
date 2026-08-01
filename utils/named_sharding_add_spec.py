
def NamedShardingAddSpec(builder, spec):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(spec), 0)

