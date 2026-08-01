
def _maybe_wrap_command_args_with_numa_binding(
    command_args: tuple[str, ...],
    *,
    gpu_index: int,
    numa_options: NumaOptions | None,
) -> tuple[str, ...]:
    """
    Wraps command arguments with numactl to apply NUMA CPU binding.

    This function prepends numactl with appropriate CPU affinity flags to the
    provided command arguments, binding the process to CPUs associated with
    the specified GPU's NUMA node.

    Args:
        command_args: The original command arguments to wrap.
        gpu_index: The index of the GPU that will be used by the subprocess.
        numa_options: Configuration for NUMA binding behavior. If None, returns
            the original command_args unchanged.

    Returns:
        Tuple of command arguments, potentially wrapped with numactl for NUMA binding.
        Returns the original command_args if numa_options is None or if binding fails
        and fallback is enabled.
    """
    if numa_options is None:
        return command_args

    kwargs = {
        "command_args": command_args,
        "gpu_index": gpu_index,
        "numa_options": asdict(numa_options),
    }

    try:
        logical_cpu_indices = _get_validated_logical_cpus_to_bind_to(
            gpu_index=gpu_index,
            numa_options=numa_options,
        )

        wrapped_command_args = _assemble_numactl_command_args(
            original_command_args=command_args,
            logical_cpu_indices=logical_cpu_indices,
        )
        signpost_event(
            category="numa_binding",
            name="apply_success",
            parameters={
                **kwargs,
                "wrapped_command": wrapped_command_args,
            },
        )
        return wrapped_command_args
    except Exception:
        # pyrefly: ignore [bad-argument-type]
        _handle_exception(numa_options=numa_options, logger_kwargs=kwargs)
        return command_args

