
def AbstractMeshAddAxisTypes(builder, axisTypes):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(axisTypes), 0)

