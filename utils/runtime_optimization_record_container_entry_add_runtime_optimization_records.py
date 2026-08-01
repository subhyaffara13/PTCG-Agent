
def RuntimeOptimizationRecordContainerEntryAddRuntimeOptimizationRecords(builder, runtimeOptimizationRecords):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(runtimeOptimizationRecords), 0)

