
def raise_unhashable(
    arg: VariableTracker, tx: "InstructionTranslator | None" = None
) -> None:
    if tx is None:
        from torch._dynamo.symbolic_convert import InstructionTranslator

        tx = InstructionTranslator.current_tx()
    try:
        arg_type = arg.python_type()
    except Exception:
        arg_type = type(arg)

    raise_observed_exception(
        TypeError,
        tx,
        args=[
            f"unhashable type: {arg_type!r} and variable tracker = {type(arg.realize())}",
        ],
    )

