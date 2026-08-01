
def module_namespace(xp: ModuleType) -> ModuleType:
    """Determine the Array API compatible namespace of the given module.

    This function is closely linked to the `array_api_compat.array_namespace` function. It returns
    the compatible namespace for a module directly instead of from an array object of that module.

    See https://data-apis.org/array-api-compat/helper-functions.html#array_api_compat.array_namespace
    """
    try:
        return array_namespace(xp.empty(0))
    except AttributeError as e:
        raise ValueError(f"Module {xp} is not an Array API compatible module.") from e

