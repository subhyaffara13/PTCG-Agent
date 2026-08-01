
def get_available_backends() -> tuple[str, ...]:
    """
    Test for the availability of built-in backends.

    :return a tuple of the built-in backend names that were successfully imported

    .. versionadded:: 4.12

    """
    available_backends: list[str] = []
    for backend_name in get_all_backends():
        try:
            get_async_backend(backend_name)
        except ImportError:
            continue

        available_backends.append(backend_name)

    return tuple(available_backends)

