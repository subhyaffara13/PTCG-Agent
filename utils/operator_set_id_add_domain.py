
def OperatorSetIdAddDomain(builder, domain):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(domain), 0)

