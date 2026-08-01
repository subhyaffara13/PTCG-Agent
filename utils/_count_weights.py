
def _count_weights(
    exported_program: torch.export.ExportedProgram,
) -> tuple[defaultdict[torch.dtype, int], defaultdict[torch.dtype, int]]:
    """Count the size of the parameters in the exported program."""

    parameter_count: defaultdict[torch.dtype, int] = defaultdict(int)
    buffer_count: defaultdict[torch.dtype, int] = defaultdict(int)
    for parameter in exported_program.parameters():
        dtype = parameter.dtype
        parameter_count[dtype] += parameter.numel()

    for buffer in exported_program.buffers():
        dtype = buffer.dtype
        buffer_count[dtype] += buffer.numel()

    return parameter_count, buffer_count

