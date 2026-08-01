
def get_current_task() -> TaskInfo:
    """
    Return the current task.

    :return: a representation of the current task
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().get_current_task()

