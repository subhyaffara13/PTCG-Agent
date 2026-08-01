
def InferenceSessionAddOrtVersion(builder, ortVersion):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(ortVersion), 0)

