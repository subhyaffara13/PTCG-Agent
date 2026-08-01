
def get_running_tasks() -> list[TaskInfo]:
    """
    Return a list of running tasks in the current event loop.

    :return: a list of task info objects
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return cast("list[TaskInfo]", get_async_backend().get_running_tasks())

