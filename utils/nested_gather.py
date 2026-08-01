
def nested_gather(tensors, parallel_mode, name=None):
    """
    Gather value of `tensors` (tensor or list/tuple of nested tensors) across processes.
    """
    from .training_args import ParallelMode

    if tensors is None:
        return
    if is_torch_xla_available():
        if name is None:
            name = "nested_gather"
        tensors = nested_xla_mesh_reduce(tensors, name)
    elif is_sagemaker_mp_enabled():
        tensors = smp_gather(tensors)
    elif parallel_mode == ParallelMode.DISTRIBUTED:
        tensors = distributed_concat(tensors)
    return tensors

