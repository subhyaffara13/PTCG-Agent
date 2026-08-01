
def RuntimeOptimizationsAddRecords(builder, records):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(records), 0)

