
def _verify_arg_name(
    stub_arg: nodes.Argument, runtime_arg: inspect.Parameter, function_name: str
) -> Iterator[str]:
    """Checks whether argument names match."""
    # Ignore exact names for most dunder methods
    if is_dunder(function_name, exclude_special=True):
        return

    if (
        stub_arg.variable.name == runtime_arg.name
        or stub_arg.variable.name.removeprefix("__") == runtime_arg.name
    ):
        return

    nonspecific_names = {"object", "args"}
    if runtime_arg.name in nonspecific_names:
        return

    def names_approx_match(a: str, b: str) -> bool:
        a = a.strip("_")
        b = b.strip("_")
        return a.startswith(b) or b.startswith(a) or len(a) == 1 or len(b) == 1

    # Be more permissive about names matching for positional-only arguments
    if runtime_arg.kind == inspect.Parameter.POSITIONAL_ONLY and names_approx_match(
        stub_arg.variable.name, runtime_arg.name
    ):
        return
    # This comes up with namedtuples, so ignore
    if stub_arg.variable.name == "_self":
        return
    yield (
        f'stub parameter "{stub_arg.variable.name}" '
        f'differs from runtime parameter "{runtime_arg.name}"'
    )

