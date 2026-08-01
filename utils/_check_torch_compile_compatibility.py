
def _check_torch_compile_compatibility(
    stages: list[_PipelineStageBase], schedule_name: str
):
    """
    Check if the schedule is compatible with torch.compile.

    Args:
        stages: List of pipeline stages to check
        schedule_name: Name of the schedule for error message

    Raises:
        RuntimeError: If any stage uses torch.compile
    """
    for stage in stages:
        if not isinstance(stage.submod, torch.nn.Module):
            continue

        for module in stage.submod.modules():
            if isinstance(module, OptimizedModule):
                raise RuntimeError(
                    f"The {schedule_name} schedule is not supported with "
                    "stage modules that have used torch.compile. "
                    f"Found OptimizedModule in {type(module).__name__}"
                )

