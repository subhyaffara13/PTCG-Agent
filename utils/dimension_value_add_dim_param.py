
def DimensionValueAddDimParam(builder, dimParam):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(dimParam), 0)

