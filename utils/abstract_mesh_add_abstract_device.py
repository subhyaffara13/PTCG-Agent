
def AbstractMeshAddAbstractDevice(builder, abstractDevice):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(abstractDevice), 0)

