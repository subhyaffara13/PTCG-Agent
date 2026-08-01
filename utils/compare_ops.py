
def compare_ops(
    program_a: torch.export.ExportedProgram, program_b: torch.export.ExportedProgram
) -> tuple[set[str], set[str]]:
    """Compare and get unique ops in two exported programs.

    Args:
        program_a: The first exported program.
        program_b: The second exported program.

    Returns:
        A tuple of two sets, where the first set contains the unique ops in the first program
        and the second set contains the unique ops in the second program.
    """
    program_a_ops = set(_count_fx_targets(program_a))
    program_b_ops = set(_count_fx_targets(program_b))
    return program_a_ops - program_b_ops, program_b_ops - program_a_ops

