
def NamedShardingAddMesh(builder, mesh):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(mesh), 0)

