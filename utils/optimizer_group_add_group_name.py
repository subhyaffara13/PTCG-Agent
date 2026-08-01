
def OptimizerGroupAddGroupName(builder, groupName):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(groupName), 0)

