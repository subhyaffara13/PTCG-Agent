import copy
from typing import Any, Callable

def get_params_from_function(func: Callable[..., Any]) -> dict[str, ParamMeta]:
    signature = inspect.signature(func, eval_str=True)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation, typer_annotations = _split_annotation_from_typer_annotations(
            param.annotation,
        )
        if len(typer_annotations) > 1:
            raise MultipleTyperAnnotationsError(param.name)

        default = param.default
        if typer_annotations:
            # It's something like `my_param: Annotated[str, Argument()]`
            [parameter_info] = typer_annotations

            # Forbid `my_param: Annotated[str, Argument()] = Argument("...")`
            if isinstance(param.default, ParameterInfo):
                raise MixedAnnotatedAndDefaultStyleError(
                    argument_name=param.name,
                    annotated_param_type=type(parameter_info),
                    default_param_type=type(param.default),
                )

            parameter_info = copy(parameter_info)

            # When used as a default, `Option` takes a default value and option names
            # as positional arguments:
            #   `Option(some_value, "--some-argument", "-s")`
            # When used in `Annotated` (ie, what this is handling), `Option` just takes
            # option names as positional arguments:
            #   `Option("--some-argument", "-s")`
            # In this case, the `default` attribute of `parameter_info` is actually
            # meant to be the first item of `param_decls`.
            if (
                isinstance(parameter_info, OptionInfo)
                and parameter_info.default is not ...
            ):
                parameter_info.param_decls = (
                    cast(str, parameter_info.default),
                    *(parameter_info.param_decls or ()),
                )
                parameter_info.default = ...

            # Forbid `my_param: Annotated[str, Argument('some-default')]`
            if parameter_info.default is not ...:
                raise AnnotatedParamWithDefaultValueError(
                    param_type=type(parameter_info),
                    argument_name=param.name,
                )
            if param.default is not param.empty:
                # Put the parameter's default (set by `=`) into `parameter_info`, where
                # typer can find it.
                parameter_info.default = param.default

            default = parameter_info
        elif param.name in type_hints:
            # Resolve forward references.
            annotation = type_hints[param.name]

        if isinstance(default, ParameterInfo):
            parameter_info = copy(default)
            # Click supports `default` as either
            # - an actual value; or
            # - a factory function (returning a default value.)
            # The two are not interchangeable for static typing, so typer allows
            # specifying `default_factory`. Move the `default_factory` into `default`
            # so click can find it.
            if parameter_info.default is ... and parameter_info.default_factory:
                parameter_info.default = parameter_info.default_factory
            elif parameter_info.default_factory:
                raise DefaultFactoryAndDefaultValueError(
                    argument_name=param.name, param_type=type(parameter_info)
                )
            default = parameter_info

        params[param.name] = ParamMeta(
            name=param.name, default=default, annotation=annotation
        )
    return params

