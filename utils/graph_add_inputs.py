
def GraphAddInputs(builder, inputs):
    builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(inputs), 0)

