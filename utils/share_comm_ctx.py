
def share_comm_ctx(modules: list[FSDPModule]) -> None:
    """
    Share cuda streams for multiple FSDPModules

    Example usage:
        from torch.distributed.fsdp import share_comm_ctx
        share_comm_ctx([fsdp_model_1, fsdp_model_2, ...])

    For Pipeline Parallelism (PP), each model chunk is a FSDP root. We want
    to share cuda streams for all-gather, reduce-scatter, and all-reduce.
    This avoids allocating inter-stream memory framgmentation

    Args:
        modules (List[FSDPModule]): modules to share cuda streams
    """
    if len(modules) == 0:
        return
    for module in modules:
        if not isinstance(module, FSDPModule):
            raise ValueError(f"Expects list of FSDPModules but got {module}")
    fsdp_states = [module._get_fsdp_state() for module in modules]
    comm_ctx = fsdp_states[0]._comm_ctx
    for fsdp_state in fsdp_states[1:]:
        fsdp_state._comm_ctx = comm_ctx
        for fsdp_param_group in fsdp_state._fsdp_param_groups:
            fsdp_param_group.comm_ctx = comm_ctx

