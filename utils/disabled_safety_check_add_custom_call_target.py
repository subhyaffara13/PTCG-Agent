
def DisabledSafetyCheckAddCustomCallTarget(builder, customCallTarget):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(customCallTarget), 0)

