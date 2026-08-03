from typing import Any

def _init_state_dict(state_dict: dict[str, Any]) -> Any:
    """
    Initializes meta tensor if the meta tensor is DTensor or torch.Tensor.
    """

    def dtensor_func(value: DTensor):
        device = getattr(value, "device", None)
        if device == torch.device("meta"):
            device_type = dist.distributed_c10d._get_pg_default_device().type
            device = cast(
                torch.device, _get_device_module(device_type).current_device()
            )
            new_local_tensor = torch.empty_like(value.to_local(), device=device)
            # We need to pass shape and stride explicitly, since DTensor might be
            # sharded unevenly.
            dtensor = DTensor.from_local(
                new_local_tensor,
                device_mesh=value.device_mesh,
                placements=value.placements,
                shape=value.size(),
                stride=value.stride(),
            )
            return dtensor
        else:
            return value

    def sharded_tensor_func(value: Any):
        device = getattr(value, "device", None)
        if device == torch.device("meta"):
            raise RuntimeError(
                f"Found unsupported type {type(value)} for meta device loading."
            )
        else:
            return value

    def tensor_func(value: torch.Tensor):
        device = getattr(value, "device", None)
        if device == torch.device("meta"):
            device_type = dist.distributed_c10d._get_pg_default_device().type
            device = cast(
                torch.device, _get_device_module(device_type).current_device()
            )
            tensor = torch.empty_like(value, device=device)
            return tensor
        else:
            return value

    _iterate_state_dict(
        state_dict,
        dtensor_func,
        sharded_tensor_func,
        tensor_func,
    )

