
def _check_flat_params_on_expected_device(state: _FSDPState, module: nn.Module):
    """
    Checks that all ``FlatParameter``s in ``module`` 's tree managed by
    ``state`` are on the expected device for *lazy initialization*.
    """
    cpu_device = torch.device("cpu")
    for handle in traversal_utils._get_fsdp_handles(module):
        if (
            not handle._offload_params
            and handle.flat_param.device != state.compute_device
        ):
            raise RuntimeError(
                "An FSDP-managed module unexpectedly has parameters on "
                f"{handle.flat_param.device}. Make sure to move the module to "
                f"{state.compute_device} before training."
            )
        elif handle._offload_params and handle.flat_param.device != cpu_device:
            raise RuntimeError(
                "An FSDP-managed module with parameter CPU offloading enabled "
                f"has parameters on {handle.flat_param.device}. Make sure to "
                f"not move the module from CPU when offloading parameters."
            )

