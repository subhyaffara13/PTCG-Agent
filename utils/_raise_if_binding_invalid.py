
def _raise_if_binding_invalid(*, logical_cpu_indices: set[int]) -> None:
    # NOTE: numactl CLI is only actually necessary for the str entrypoint path,
    # but for simplicity we will just check it no matter what.
    if shutil.which("numactl") is None:
        raise RuntimeError("numactl CLI is required for NUMA binding")

    if not logical_cpu_indices:
        raise RuntimeError("Must bind to a non-empty set of CPU indices")

