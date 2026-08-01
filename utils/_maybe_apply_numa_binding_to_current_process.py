
def _maybe_apply_numa_binding_to_current_process(
    *, gpu_index: int, numa_options: NumaOptions
) -> None:
    kwargs = {
        "gpu_index": gpu_index,
        "numa_options": asdict(numa_options),
    }

    try:
        logical_cpu_indices = _get_validated_logical_cpus_to_bind_to(
            gpu_index=gpu_index,
            numa_options=numa_options,
        )

        _bind_all_threads_in_current_process_to_logical_cpus(
            logical_cpu_indices=logical_cpu_indices
        )

        signpost_event(
            category="numa_binding",
            name="apply_success",
            parameters={
                **kwargs,
                "logical_cpu_indices": _get_ranges_str_from_ints(logical_cpu_indices),
            },
        )
    except Exception:
        # pyrefly: ignore [bad-argument-type]
        _handle_exception(numa_options=numa_options, logger_kwargs=kwargs)

