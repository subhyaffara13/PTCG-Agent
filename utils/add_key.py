
def AddKey(builder, key):
    StringStringEntryAddKey(builder, key)


def AddKey(builder, key):  # noqa: N802
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(key), 0)

