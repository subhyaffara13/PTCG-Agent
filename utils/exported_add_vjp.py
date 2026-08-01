
def ExportedAddVjp(builder, vjp):
    builder.PrependUOffsetTRelativeSlot(17, flatbuffers.number_types.UOffsetTFlags.py_type(vjp), 0)

