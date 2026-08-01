
def _worker_compile_triton(
    load_kernel: Callable[[], CachingAutotuner],
    extra_env: dict[str, str],
    extra_config: dict[str, Any],
) -> tuple[CachingAutotuner, int]:
    _set_triton_ptxas_path()
    os.environ.update(extra_env)
    # Set libdevice path if passed via env from main process
    libdevice_path = extra_env.get("TRITON_LIBDEVICE_PATH")
    if libdevice_path:
        try:
            from triton import knobs

            knobs.nvidia.libdevice_path = libdevice_path
        except ImportError:
            pass
    from torch._inductor import config

    with config.patch(extra_config):
        fail = None
        try:
            start_ns = time.time_ns()
            kernel = load_kernel()
            kernel.precompile(warm_cache_only=True)
            elapsed_ns = time.time_ns() - start_ns
            kernel.prepare_for_pickle()
            # We can release this memory in the compile subprocesses:
            linecache.clearcache()
            return kernel, elapsed_ns // 1000
        except Exception as e:
            fail = str(e)
            raise
        finally:
            log_triton_builds(fail=fail)

