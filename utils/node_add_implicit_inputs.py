
def NodeAddImplicitInputs(builder, implicitInputs):
    builder.PrependUOffsetTRelativeSlot(12, flatbuffers.number_types.UOffsetTFlags.py_type(implicitInputs), 0)

