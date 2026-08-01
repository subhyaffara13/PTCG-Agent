
def AbstractDeviceAddDeviceKind(builder, deviceKind):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(deviceKind), 0)

