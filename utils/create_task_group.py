
def create_task_group() -> TaskGroup:
    """
    Create a task group.

    :return: a task group
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().create_task_group()

