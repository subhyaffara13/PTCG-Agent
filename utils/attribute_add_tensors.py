
def AttributeAddTensors(builder, tensors):
    builder.PrependUOffsetTRelativeSlot(11, flatbuffers.number_types.UOffsetTFlags.py_type(tensors), 0)

