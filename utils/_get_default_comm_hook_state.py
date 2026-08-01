
def _get_default_comm_hook_state(
    process_group: dist.ProcessGroup,
) -> default_hooks.DefaultState:
    return default_hooks.DefaultState(process_group=process_group)

