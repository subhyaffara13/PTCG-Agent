
def run_multithreaded(closure, max_workers, arguments=None, pass_barrier=False):
    with ThreadPoolExecutor(max_workers=max_workers) as tpe:
        if arguments is None:
            arguments = []
        else:
            arguments = list(arguments)

        if pass_barrier:
            barrier = threading.Barrier(max_workers)
            arguments.append(barrier)

        try:
            futures = []
            for _ in range(max_workers):
                futures.append(tpe.submit(closure, *arguments))  # noqa: PERF401
        except RuntimeError as e:
            import pytest

            pytest.skip(
                f"Spawning {max_workers} threads failed with "
                f"error {e!r} (likely due to resource limits on the "
                "system running the tests)"
            )
        finally:
            if len(futures) < max_workers and pass_barrier:
                barrier.abort()
        for f in futures:
            f.result()

