
def get_tma_workspace_arg(
    num_tma_descriptors: int,
    device: torch.device,
    num_programs: int | None = None,
) -> WorkspaceArg:
    """Builds and returns a WorkspaceArg for the device side TMA workspace buffer."""
    from .codegen.common import WorkspaceArg, WorkspaceZeroMode

    if num_programs is None:
        num_programs = get_num_sms()
    zero_mode = WorkspaceZeroMode.from_bool(False)
    size = num_programs * num_tma_descriptors * TMA_DESCRIPTOR_SIZE
    return WorkspaceArg(
        count=size,
        zero_mode=zero_mode,
        device=device,
        outer_name=WorkspaceArg.unique_name(),
    )

