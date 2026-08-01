
def can_be_positional(param: Parameter) -> bool:
    """Return whether the parameter accepts a positional argument.

    ```python {test="skip" lint="skip"}
    def func(a, /, b, *, c):
        pass

    params = inspect.signature(func).parameters
    can_be_positional(params['a'])
    #> True
    can_be_positional(params['b'])
    #> True
    can_be_positional(params['c'])
    #> False
    ```
    """
    return param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)

