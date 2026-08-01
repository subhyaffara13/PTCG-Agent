
def CheckpointAddOptimizerGroups(builder, optimizerGroups):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(optimizerGroups), 0)

