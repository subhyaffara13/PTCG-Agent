
def NodeAddInputs(builder, inputs):
    builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(inputs), 0)

