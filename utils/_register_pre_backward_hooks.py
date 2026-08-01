
def _register_pre_backward_hooks(
    state: _FSDPState,
    module: nn.Module,
    outputs: Any,
    handle: FlatParamHandle,
) -> None:
    """
    Registers pre-backward hooks on the tensors that require gradients in the
    forward pass outputs ``outputs``, which were computed using the
    ``FlatParameter`` s of ``handles``.

    Args:
        module (nn.Module): Fully sharded module (see [Note: Fully Sharded
            Module]).

    Returns:
        Forward pass outputs with pre-backward hooks registered to tensors that
        require gradients.
    """
    # If there is no gradient computation, then there is no need for
    # pre-backward logic
    if not torch.is_grad_enabled():
        return outputs
    if state._is_root:
        state._post_backward_callback_queued = False  # only defined on the root

    if handle:
        handle._needs_pre_backward_unshard = False
        # Since these handles' `FlatParameter`s participated in a forward, we
        # conservatively assume that they will be used in the backward
        handle._ran_pre_backward_hook = False

    def _register_hook(t: torch.Tensor) -> torch.Tensor:
        if t.requires_grad:
            t.register_hook(
                torch.utils.hooks.unserializable_hook(
                    functools.partial(_pre_backward_hook, state, module, handle)
                )
            )
            if handle:
                handle._needs_pre_backward_unshard = True
        return t

    return _apply_to_tensors(_register_hook, outputs)

