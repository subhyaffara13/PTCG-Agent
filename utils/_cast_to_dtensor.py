
def _cast_to_dtensor(
    tensor, placements: tuple[Placement, ...], mesh: DeviceMesh
) -> DTensor:
    if isinstance(tensor, DTensor):
        if tensor.placements == placements:
            return tensor
        else:
            raise RuntimeError(f"Expected {placements} but got {tensor.placements}.")
    elif isinstance(tensor, torch.Tensor):
        return DTensor.from_local(
            tensor, device_mesh=mesh, placements=placements, run_check=False
        )
    else:
        raise TypeError(f"Unsupported type {type(tensor)}")

