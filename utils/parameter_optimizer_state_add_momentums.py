
def ParameterOptimizerStateAddMomentums(builder, momentums):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(momentums), 0)

