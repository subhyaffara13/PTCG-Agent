
def CheckpointAddPropertyBag(builder, propertyBag):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(propertyBag), 0)

