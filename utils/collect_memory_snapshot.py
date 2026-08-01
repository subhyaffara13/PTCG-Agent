
def collect_memory_snapshot(
    benchmark_compiled_module_fn: BenchmarkCallableType,
) -> None:
    assert torch.cuda.is_available()

    torch.cuda.memory._record_memory_history(max_entries=100000)
    benchmark_compiled_module_fn(times=10, repeat=1)  # run 10 times
    snapshot_path = f"{tempfile.gettempdir()}/memory_snapshot.pickle"
    torch.cuda.memory._dump_snapshot(snapshot_path)
    torch.cuda.memory._record_memory_history(enabled=None)
    print(f"The collect memory snapshot has been written to {snapshot_path}")

