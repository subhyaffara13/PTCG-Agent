
def AddDict(builder, dict):  # noqa: N802
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(dict), 0)

