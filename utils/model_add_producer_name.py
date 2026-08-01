
def ModelAddProducerName(builder, producerName):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(producerName), 0)

