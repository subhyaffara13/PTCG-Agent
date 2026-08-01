
def AbstractDeviceAddPlatform(builder, platform):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(platform), 0)

