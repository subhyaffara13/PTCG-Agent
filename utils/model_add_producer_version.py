
def ModelAddProducerVersion(builder, producerVersion):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(producerVersion), 0)

