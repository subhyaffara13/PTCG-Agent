
def OptimizerGroupAddOptimizerStates(builder, optimizerStates):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(optimizerStates), 0)

