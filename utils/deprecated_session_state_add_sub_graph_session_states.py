
def DeprecatedSessionStateAddSubGraphSessionStates(builder, subGraphSessionStates):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(subGraphSessionStates), 0)

