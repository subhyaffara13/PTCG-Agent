
def perf_profile(
    wall_time_ms: float,
    times: int,
    repeat: int,
    benchmark_name: str,
    benchmark_compiled_module_fn: BenchmarkCallableType,
) -> None:
    with torch.profiler.profile(record_shapes=True) as p:
        benchmark_compiled_module_fn(times=times, repeat=repeat)

    path = PROFILE_PATH
    p.export_chrome_trace(path)
    print(f"Profiling result for a compiled module of benchmark {benchmark_name}:")
    print(f"Chrome trace for the profile is written to {path}")
    event_list = p.key_averages(group_by_input_shape=True)
    print(event_list.table(sort_by="self_device_time_total", row_limit=10))
    parse_profile_event_list(
        benchmark_name, event_list, wall_time_ms, times * repeat, p.use_device or ""
    )

