
def ValueInfoAddType(builder, type):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(type), 0)

