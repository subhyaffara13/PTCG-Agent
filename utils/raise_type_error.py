
def raise_type_error(tx: InstructionTranslatorBase, msg: str) -> NoReturn:
    """Raise a TypeError as an observed exception during tracing."""
    raise_observed_exception(TypeError, tx, args=[msg])

