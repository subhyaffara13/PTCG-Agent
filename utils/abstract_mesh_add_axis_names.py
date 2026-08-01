
def AbstractMeshAddAxisNames(builder, axisNames):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(axisNames), 0)

