
def RuntimeOptimizationRecordAddProducedOpIds(builder, producedOpIds):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(producedOpIds), 0)

