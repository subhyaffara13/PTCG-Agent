
def device_hint(tensor) -> "str":
    if isinstance(tensor, torch._subclasses.FakeTensor):
        return tensor.fake_device.type
    elif (
        hasattr(tensor, "device")
        and hasattr(tensor.device, "type")
        and tensor.device.type != "meta"
    ):
        return tensor.device.type
    else:
        return "cuda"  # default to cuda

