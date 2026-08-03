from typing import Any

def create_default_local_save_plan(
    state_dict: dict[str, Any], is_coordinator: bool
) -> SavePlan:
    """
    Create the ``SavePlan`` used by DefaultSavePlanner.

    On non-coordinator ranks, this function ignores tensors and non-tensor objects,
    only producing writes for ShardedTensor objects.

    On the coordinator rank, produce writes for all values.
    """
    requests = []
    for fqn, obj in state_dict.items():
        # Since DTensor supports submesh, adding extra check to ensure _create_write_items()
        # gets called only when the current rank is part of the mesh for the corresponding DTensor.
        if isinstance(obj, DTensor):
            if obj.device_mesh.get_coordinate() is not None:
                requests += _create_write_items(fqn, obj)
        else:
            # For the plain tensor and non-tensor values, add the request for all
            # the ranks. Coordinator will decides whether to deduplicate the
            # values based on the keys.
            requests += _create_write_items(fqn, obj)

    return SavePlan(requests)

