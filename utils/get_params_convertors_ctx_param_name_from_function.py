from typing import Any, Callable

def get_params_convertors_ctx_param_name_from_function(
    callback: Callable[..., Any] | None,
) -> tuple[list[click.Argument | click.Option], dict[str, Any], str | None]:
    params = []
    convertors = {}
    context_param_name = None
    if callback:
        parameters = get_params_from_function(callback)
        for param_name, param in parameters.items():
            if lenient_issubclass(param.annotation, click.Context):
                context_param_name = param_name
                continue
            click_param, convertor = get_click_param(param)
            if convertor:
                convertors[param_name] = convertor
            params.append(click_param)
    return params, convertors, context_param_name

