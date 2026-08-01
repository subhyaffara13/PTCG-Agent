
def InferenceSessionAddModel(builder, model):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(model), 0)

