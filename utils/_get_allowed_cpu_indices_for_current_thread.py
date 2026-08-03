import os

def _get_allowed_cpu_indices_for_current_thread() -> set[int]:
    # 0 denotes current thread
    # pyrefly: ignore [missing-attribute]
    return os.sched_getaffinity(0)  # type:ignore[attr-defined]

