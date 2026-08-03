from typing import Any, Dict, Optional

def _get_process_memory_info(
    worker_pid: int, include_process_info: bool
) -> Optional[Dict[str, Any]]:
    """Get process-level memory information using psutil."""
    if not include_process_info:
        return None

    try:
        import psutil

        process = psutil.Process()
        memory_info = process.memory_info()
        ram_usage_mb = round(memory_info.rss / (1024 * 1024), 2)
        virtual_memory_mb = round(memory_info.vms / (1024 * 1024), 2)
        memory_percent = round(process.memory_percent(), 2)

        return {
            "pid": worker_pid,
            "summary": f"Worker PID {worker_pid} using {ram_usage_mb:.1f} MB of RAM ({memory_percent:.1f}% of system memory)",
            "ram_usage": {
                "megabytes": ram_usage_mb,
                "description": "Actual physical RAM used by this process",
            },
            "virtual_memory": {
                "megabytes": virtual_memory_mb,
                "description": "Total virtual memory allocated (includes swapped memory)",
            },
            "system_memory_percent": {
                "percent": memory_percent,
                "description": "Percentage of total system RAM being used",
            },
            "open_file_handles": {
                "count": (
                    process.num_fds()
                    if hasattr(process, "num_fds")
                    else "N/A (Windows)"
                ),
                "description": "Number of open file descriptors/handles",
            },
            "threads": {
                "count": process.num_threads(),
                "description": "Number of active threads in this process",
            },
        }
    except ImportError:
        return {
            "pid": worker_pid,
            "error": "psutil not installed. Install with: pip install psutil",
        }
    except Exception as e:
        verbose_proxy_logger.debug(f"Error getting process info: {e}")
        return {"pid": worker_pid, "error": str(e)}

