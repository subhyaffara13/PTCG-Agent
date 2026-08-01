
def CheckpointAddModuleState(builder, moduleState):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(moduleState), 0)

