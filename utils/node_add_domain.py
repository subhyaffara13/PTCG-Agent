
def NodeAddDomain(builder, domain):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(domain), 0)

