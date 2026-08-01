
def _describe_arg_for_logging(arg: object) -> str:
    from torch._library import opaque_object

    try:
        is_dtensor = isinstance(arg, torch.distributed.tensor.DTensor)
    except AttributeError:
        is_dtensor = False

    if is_dtensor:
        arg = typing.cast(torch.distributed.tensor.DTensor, arg)
        mesh = arg.device_mesh
        return (
            f"DTensor(shape={arg.shape}, dtype={arg.dtype}, "
            f"device={arg.device}, mesh_shape={mesh.shape}, "
            f"placements={arg.placements})"
        )
    elif isinstance(arg, torch.Tensor):
        return f"Tensor(shape={arg.shape}, dtype={arg.dtype}, device={arg.device})"
    elif opaque_object.is_opaque_type(type(arg)):
        return f"Opaque: {type(arg).__name__}"
    else:
        return f"{type(arg).__name__}: {arg}"

