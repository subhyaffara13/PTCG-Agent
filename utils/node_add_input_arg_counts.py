
def NodeAddInputArgCounts(builder, inputArgCounts):
    builder.PrependUOffsetTRelativeSlot(11, flatbuffers.number_types.UOffsetTFlags.py_type(inputArgCounts), 0)

