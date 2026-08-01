
def zip_arguments(
    schema: torch.FunctionSchema, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> Iterator[tuple[torch.Argument, Any]]:
    schema_args = schema.arguments[: len(args)]
    schema_kwargs = {arg.name: arg for arg in schema.arguments[len(args) :]}

    yield from zip(schema_args, args)

    for _, argument, value in zip_by_key(schema_kwargs, kwargs):
        yield (argument, value)

