
def block_pipeline_command(name: str) -> Callable[..., Any]:
    """
    Prints error because some pipelined commands should
    be blocked when running in cluster-mode
    """

    def inner(*args, **kwargs):
        raise RedisClusterException(
            f"ERROR: Calling pipelined function {name} is blocked "
            f"when running redis in cluster mode..."
        )

    return inner

