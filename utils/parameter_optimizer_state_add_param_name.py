
def ParameterOptimizerStateAddParamName(builder, paramName):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(paramName), 0)

