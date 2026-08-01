
def RuntimeOptimizationRecordAddActionId(builder, actionId):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(actionId), 0)

