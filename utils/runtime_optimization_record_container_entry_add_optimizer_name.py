
def RuntimeOptimizationRecordContainerEntryAddOptimizerName(builder, optimizerName):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(optimizerName), 0)

