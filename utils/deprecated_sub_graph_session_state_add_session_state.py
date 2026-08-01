
def DeprecatedSubGraphSessionStateAddSessionState(builder, sessionState):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(sessionState), 0)

