import os

def _bind_all_threads_in_current_process_to_logical_cpus(
    *, logical_cpu_indices: set[int]
) -> None:
    # Save the original affinity of the main thread before changing it
    # pyrefly: ignore [missing-attribute]
    original_main_thread_affinity = os.sched_getaffinity(0)  # type: ignore[attr-defined]

    # 0 represents the current thread.
    # This is outside the try/except because the main thread should always bind successfully.
    # pyrefly: ignore [missing-attribute]
    os.sched_setaffinity(0, logical_cpu_indices)  # type: ignore[attr-defined]

    for tid_str in os.listdir("/proc/self/task"):
        try:
            tid = int(tid_str)
            # pyrefly: ignore [missing-attribute]
            tid_affinity = os.sched_getaffinity(tid)  # type: ignore[attr-defined]

            # Defensive check to ensure we do not overwrite affinity on any threads
            # that have already had their affinity set elsewhere.
            if tid_affinity == original_main_thread_affinity:
                # pyrefly: ignore [missing-attribute]
                os.sched_setaffinity(tid, logical_cpu_indices)  # type: ignore[attr-defined]
        except Exception:
            # Thread may have exited or otherwise become invalid
            pass

