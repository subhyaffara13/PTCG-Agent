from typing import Optional

def _verify_param_shape_across_processes(
    process_group: dist.ProcessGroup,
    tensors: list[torch.Tensor],
    logger: Optional["dist.Logger"] = None,
):
    return dist._verify_params_across_processes(process_group, tensors, logger)

