from typing import Any, Callable

def get_param_completion(
    callback: Callable[..., Any] | None = None,
) -> Callable[..., Any] | None:
    if not callback:
        return None
    parameters = get_params_from_function(callback)
    ctx_name = None
    args_name = None
    incomplete_name = None
    unassigned_params = list(parameters.values())
    for param_sig in unassigned_params[:]:
        origin = get_origin(param_sig.annotation)
        if lenient_issubclass(param_sig.annotation, click.Context):
            ctx_name = param_sig.name
            unassigned_params.remove(param_sig)
        elif lenient_issubclass(origin, list):
            args_name = param_sig.name
            unassigned_params.remove(param_sig)
        elif lenient_issubclass(param_sig.annotation, str):
            incomplete_name = param_sig.name
            unassigned_params.remove(param_sig)
    # If there are still unassigned parameters (not typed), extract by name
    for param_sig in unassigned_params[:]:
        if ctx_name is None and param_sig.name == "ctx":
            ctx_name = param_sig.name
            unassigned_params.remove(param_sig)
        elif args_name is None and param_sig.name == "args":
            args_name = param_sig.name
            unassigned_params.remove(param_sig)
        elif incomplete_name is None and param_sig.name == "incomplete":
            incomplete_name = param_sig.name
            unassigned_params.remove(param_sig)
    # Extract value param name first
    if unassigned_params:
        show_params = " ".join([param.name for param in unassigned_params])
        raise click.ClickException(
            f"Invalid autocompletion callback parameters: {show_params}"
        )

    def wrapper(ctx: click.Context, args: list[str], incomplete: str | None) -> Any:
        use_params: dict[str, Any] = {}
        if ctx_name:
            use_params[ctx_name] = ctx
        if args_name:
            use_params[args_name] = args
        if incomplete_name:
            use_params[incomplete_name] = incomplete
        return callback(**use_params)

    update_wrapper(wrapper, callback)
    return wrapper

