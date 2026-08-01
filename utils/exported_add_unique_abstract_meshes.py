
def ExportedAddUniqueAbstractMeshes(builder, uniqueAbstractMeshes):
    builder.PrependUOffsetTRelativeSlot(20, flatbuffers.number_types.UOffsetTFlags.py_type(uniqueAbstractMeshes), 0)

