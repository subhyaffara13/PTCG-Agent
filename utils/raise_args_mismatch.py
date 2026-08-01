
def raise_args_mismatch(
    tx: InstructionTranslatorBase,
    name: str,
    expect: str = "",
    actual: str = "",
) -> None:
    from torch._dynamo.exc import raise_observed_exception

    msg_str = (
        f"wrong number of arguments or keyword arguments for {name}() call.\n"
        f"  Expect: {expect}\n"
        f"  Actual: {actual}"
    )

    raise_observed_exception(
        TypeError,
        tx,
        args=[msg_str],
    )

