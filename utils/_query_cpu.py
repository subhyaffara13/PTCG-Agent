from pathlib import Path


def _query_cpu() -> int | None:
    """Try to determine number of CPUs allotted in a docker container.

    This is based on discussion and copied from suggestions in
    https://bugs.python.org/issue36054.
    """
    if Path("/sys/fs/cgroup/cpu.max").is_file():
        avail_cpu = _query_cpu_cgroupv2()
    else:
        avail_cpu = _query_cpu_cgroupsv1()
    return _query_cpu_handle_k8s_pods(avail_cpu)

