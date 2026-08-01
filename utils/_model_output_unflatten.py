
def _model_output_unflatten(
    values: Iterable[Any],
    context: list[str],
    output_type: type[ModelOutput] | None = None,
) -> ModelOutput:
    return output_type(**dict(zip(context, values)))

