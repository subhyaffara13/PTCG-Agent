
def measure_memory(is_gpu, func, monitor_type="cuda", start_memory=None):
    memory_monitor_type = None
    if monitor_type == "rocm":
        memory_monitor_type = RocmMemoryMonitor
    else:
        memory_monitor_type = CudaMemoryMonitor

    monitor = memory_monitor_type(False)

    if is_gpu:
        if start_memory is not None:
            memory_before_test = start_memory
        else:
            memory_before_test = monitor.measure_gpu_usage()
        if memory_before_test is None:
            return None

        if func is None:
            return memory_before_test

        with ThreadPoolExecutor() as executor:
            monitor = memory_monitor_type()
            mem_thread = executor.submit(monitor.measure_gpu_usage)
            try:
                fn_thread = executor.submit(func)
                _ = fn_thread.result()
            finally:
                monitor.keep_measuring = False
                max_usage = mem_thread.result()

            if max_usage is None:
                return None

            logger.info(f"GPU memory usage: before={memory_before_test}  peak={max_usage}")
            if len(memory_before_test) >= 1 and len(max_usage) >= 1 and len(memory_before_test) == len(max_usage):
                # When there are multiple GPUs, we will check the one with maximum usage.
                max_used = 0
                for i, memory_before in enumerate(memory_before_test):
                    before = memory_before["max_used_MB"]
                    after = max_usage[i]["max_used_MB"]
                    used = after - before
                    max_used = max(max_used, used)
                return max_used
        return None

    # CPU memory
    if start_memory is not None:
        memory_before_test = start_memory
    else:
        memory_before_test = monitor.measure_cpu_usage()

    if func is None:
        return memory_before_test

    with ThreadPoolExecutor() as executor:
        monitor = memory_monitor_type()
        mem_thread = executor.submit(monitor.measure_cpu_usage)
        try:
            fn_thread = executor.submit(func)
            _ = fn_thread.result()
        finally:
            monitor.keep_measuring = False
            max_usage = mem_thread.result()

        logger.info(f"CPU memory usage: before={memory_before_test:.1f} MB, peak={max_usage:.1f} MB")
        return max_usage - memory_before_test

