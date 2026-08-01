
def ModelAddDomain(builder, domain):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(domain), 0)

