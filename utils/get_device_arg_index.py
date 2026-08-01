
def get_device_arg_index(schema: _C.FunctionSchema) -> int | None:
    """
    Given a schema, returns the id of the `device: torch.device` argument.
    If it does not exist, returns None.
    """
    for index, arg in enumerate(schema.arguments):
        if arg.type is _C.DeviceObjType.get() and arg.name == "device":
            return index
    return None

