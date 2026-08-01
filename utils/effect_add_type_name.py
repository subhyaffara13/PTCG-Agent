
def EffectAddTypeName(builder, typeName):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(typeName), 0)

