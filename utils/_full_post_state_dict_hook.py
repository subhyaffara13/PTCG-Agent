
def _full_post_state_dict_hook(
    module: nn.Module,
    fsdp_state: _FSDPState,
    state_dict: dict[str, Any],
    prefix: str,
) -> dict[str, Any]:
    """
    Hook that runs after model.state_dict() is called before returning result to
    user. For FSDP, we may have to clone the tensors in state_dict as params go
    back to sharded version after _unshard_fsdp_state_params ends, and also remove
    the ``FSDP_WRAPPED_MODULE`` prefix.
    """

    def param_hook(
        state_dict: dict[str, Any],
        prefix: str,
        fqn: str,
    ) -> None:
        clean_key = fqn
        clean_prefix = clean_tensor_name(prefix)
        # Strip prefix out of key if needed as buffer names and param names
        # do not have prefix considered as they are not computed in `state_dict`
        # call.
        clean_key = clean_key.removeprefix(clean_prefix)

        # Clone parameters before exiting the `_unshard_fsdp_state_params()` context.
        if not getattr(state_dict[fqn], "_has_been_cloned", False):
            try:
                state_dict[fqn] = state_dict[fqn].detach().clone()
                state_dict[fqn]._has_been_cloned = True  # type: ignore[attr-defined]
            except BaseException as e:  # noqa: B036
                warnings.warn(
                    f"Failed to clone() tensor with name {fqn} on rank {fsdp_state.rank}. "
                    "This may mean that this state_dict entry could point to invalid "
                    "memory regions after returning from state_dict() call if this "
                    "parameter is managed by FSDP. Please check clone "
                    f"implementation of {fqn}. Error: {str(e)}",
                    stacklevel=2,
                )

    return _common_unshard_post_state_dict_hook(
        module, fsdp_state, state_dict, prefix, param_hook
    )

