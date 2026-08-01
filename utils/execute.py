
def execute(
    gm: GraphModule,
    *args: Unpack[Ts],
    executor: str = "aten",
    executor_parameters: dict | None = None,
) -> Any:
    """
    Prototype ATen executor.

    Just executes the context's graph.
    """

    if executor == "aten":
        return gm.forward(*args)

    msg = f"Received unexpected value for 'executor': {executor}. Allowed values are: aten."
    raise ValueError(msg)


def execute(
    func: Callable[[Unpack[_Ts]], object],
    args: tuple[Unpack[_Ts]],
    msg: object = None,
    verbose: bool = False,
) -> None:
    """
    Perform some action that affects the outside world (e.g. by
    writing to the filesystem). Was previously used to deal with
    "dry run" operations, but now runs unconditionally.
    """
    if msg is None:
        msg = f"{func.__name__}{args!r}"
        if msg[-2:] == ',)':  # correct for singleton tuple
            msg = msg[0:-2] + ')'

    log.info(msg)
    func(*args)

