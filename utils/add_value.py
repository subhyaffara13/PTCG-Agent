
def AddValue(builder, value):
    DimensionAddValue(builder, value)


def AddValue(builder, value):
    FloatPropertyAddValue(builder, value)


def AddValue(builder, value):
    IntPropertyAddValue(builder, value)


def AddValue(builder, value):
    StringPropertyAddValue(builder, value)


def AddValue(builder, value):
    StringStringEntryAddValue(builder, value)


def AddValue(builder, value):
    TypeInfoAddValue(builder, value)


def AddValue(builder, value):  # noqa: N802
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(value), 0)

