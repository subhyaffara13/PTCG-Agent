
def get_callback(
    *,
    callback: Callable[..., Any] | None = None,
    params: Sequence[click.Parameter] = [],
    convertors: dict[str, Callable[[str], Any]] | None = None,
    context_param_name: str | None = None,
    pretty_exceptions_short: bool,
) -> Callable[..., Any] | None:
    use_convertors = convertors or {}
    if not callback:
        return None
    parameters = get_params_from_function(callback)
    use_params: dict[str, Any] = {}
    for param_name in parameters:
        use_params[param_name] = None
    for param in params:
        if param.name:
            use_params[param.name] = param.default

    def wrapper(**kwargs: Any) -> Any:
        _rich_traceback_guard = pretty_exceptions_short  # noqa: F841
        for k, v in kwargs.items():
            if k in use_convertors:
                use_params[k] = use_convertors[k](v)
            else:
                use_params[k] = v
        if context_param_name:
            use_params[context_param_name] = click.get_current_context()
        return callback(**use_params)

    update_wrapper(wrapper, callback)
    return wrapper

