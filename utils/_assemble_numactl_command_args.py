
def _assemble_numactl_command_args(
    *, original_command_args: tuple[str, ...], logical_cpu_indices: set[int]
) -> tuple[str, ...]:
    return (
        "numactl",
        f"--physcpubind={_get_ranges_str_from_ints(logical_cpu_indices)}",
        *original_command_args,
    )

