
def _get_socket_index_for_cpu(*, cpu_index: int) -> int:
    package_id_absolute_path = (
        f"/sys/devices/system/cpu/cpu{cpu_index}/topology/physical_package_id"
    )
    try:
        with open(package_id_absolute_path) as f:
            return int(f.read().strip())
    except FileNotFoundError as e:
        raise RuntimeError(f"Could not determine socket for {cpu_index=}") from e

