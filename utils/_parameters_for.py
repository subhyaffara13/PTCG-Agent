from typing import Any

def _parameters_for(func: Any) -> dict[str, bool]:
    """Return the parameters for the plugin.

    This will inspect the plugin and return either the function parameters
    if the plugin is a function or the parameters for ``__init__`` after
    ``self`` if the plugin is a class.

    :returns:
        A dictionary mapping the parameter name to whether or not it is
        required (a.k.a., is positional only/does not have a default).
    """
    is_class = not inspect.isfunction(func)
    if is_class:
        func = func.__init__

    parameters = {
        parameter.name: parameter.default is inspect.Parameter.empty
        for parameter in inspect.signature(func).parameters.values()
        if parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    }

    if is_class:
        parameters.pop("self", None)

    return parameters

