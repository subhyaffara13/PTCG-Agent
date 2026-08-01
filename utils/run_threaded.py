
def run_threaded(func, max_workers=8, pass_count=False,
                 pass_barrier=False, outer_iterations=1,
                 prepare_args=None):
    """Runs a function many times in parallel"""
    for _ in range(outer_iterations):
        with (concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
              as tpe):
            if prepare_args is None:
                args = []
            else:
                args = prepare_args()
            if pass_barrier:
                barrier = threading.Barrier(max_workers)
                args.append(barrier)
            if pass_count:
                all_args = [(func, i, *args) for i in range(max_workers)]
            else:
                all_args = [(func, *args) for i in range(max_workers)]
            try:
                futures = []
                for arg in all_args:
                    futures.append(tpe.submit(*arg))
            except RuntimeError as e:
                import pytest
                pytest.skip(f"Spawning {max_workers} threads failed with "
                            f"error {e!r} (likely due to resource limits on the "
                            "system running the tests)")
            finally:
                if len(futures) < max_workers and pass_barrier:
                    barrier.abort()
            for f in futures:
                f.result()

