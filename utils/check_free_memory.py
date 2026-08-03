import os

def check_free_memory(free_bytes):
    """
    Check whether `free_bytes` amount of memory is currently free.
    Returns: None if enough memory available, otherwise error message
    """
    env_var = "NPY_AVAILABLE_MEM"
    env_value = os.environ.get(env_var)
    if env_value is not None:
        try:
            mem_free = _parse_size(env_value)
        except ValueError as exc:
            raise ValueError(  # noqa: B904
                f"Invalid environment variable {env_var}: {exc}"
            )

        msg = (
            f"{free_bytes / 1e9} GB memory required, but environment variable "
            f"NPY_AVAILABLE_MEM={env_value} set"
        )
    else:
        mem_free = _get_mem_available()

        if mem_free is None:
            msg = (
                "Could not determine available memory; set NPY_AVAILABLE_MEM "
                "environment variable (e.g. NPY_AVAILABLE_MEM=16GB) to run "
                "the test."
            )
            mem_free = -1
        else:
            msg = f"{free_bytes / 1e9} GB memory required, but {mem_free / 1e9} GB available"

    return msg if mem_free < free_bytes else None


def check_free_memory(free_mb):
    """
    Check *free_mb* of memory is available, otherwise do pytest.skip
    """
    import pytest

    try:
        mem_free = _parse_size(os.environ['SCIPY_AVAILABLE_MEM'])
        msg = '{} MB memory required, but environment SCIPY_AVAILABLE_MEM={}'.format(
            free_mb, os.environ['SCIPY_AVAILABLE_MEM'])
    except KeyError:
        mem_free = _get_mem_available()
        if mem_free is None:
            pytest.skip("Could not determine available memory; set SCIPY_AVAILABLE_MEM "
                        "variable to free memory in MB to run the test.")
        msg = f'{free_mb} MB memory required, but {mem_free/1e6} MB available'

    if mem_free < free_mb * 1e6:
        pytest.skip(msg)


def check_free_memory(free_bytes):
    """
    Check whether `free_bytes` amount of memory is currently free.
    Returns: None if enough memory available, otherwise error message
    """
    env_var = 'NPY_AVAILABLE_MEM'
    env_value = os.environ.get(env_var)
    if env_value is not None:
        try:
            mem_free = _parse_size(env_value)
        except ValueError as exc:
            raise ValueError(f'Invalid environment variable {env_var}: {exc}')

        msg = (f'{free_bytes / 1e9} GB memory required, but environment variable '
               f'NPY_AVAILABLE_MEM={env_value} set')
    else:
        mem_free = _get_mem_available()

        if mem_free is None:
            msg = ("Could not determine available memory; set NPY_AVAILABLE_MEM "
                   "environment variable (e.g. NPY_AVAILABLE_MEM=16GB) to run "
                   "the test.")
            mem_free = -1
        else:
            free_bytes_gb = free_bytes / 1e9
            mem_free_gb = mem_free / 1e9
            msg = f'{free_bytes_gb} GB memory required, but {mem_free_gb} GB available'

    return msg if mem_free < free_bytes else None

