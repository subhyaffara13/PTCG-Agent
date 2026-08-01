
def augment_model_with_bundled_inputs(
        model: torch.jit.ScriptModule,
        inputs: Sequence[tuple[Any, ...]] | None = None,
        _receive_inflate_expr: list[str] | None = None,  # For debugging.
        info: list[str] | None = None,  # Optional argument to provide info about forward or its inputs
        skip_size_check=False,
) -> None:
    """Add bundled sample inputs to a model for the forward function.

    Models with bundled inputs can be invoked in a uniform manner by
    benchmarking and code coverage tools.

    Augmented models will support the following methods:

        `get_all_bundled_inputs() -> List[Tuple[Any, ...]]`
            Returns a list of tuples suitable for passing to the model like
            `for inp in model.get_all_bundled_inputs(): model(*inp)`

        `get_num_bundled_inputs() -> int`
            Equivalent to `len(model.get_all_bundled_inputs())`,
            but slightly easier to call from C++.

        `get_bundled_inputs_functions_and_info() -> Dict[str, Dict[str: List[str]]]`
            Returns a dictionary mapping function names to a metadata dictionary.
            This nested dictionary maps preset strings like:
                'get_inputs_function_name' -> the name of a function attribute in this model that can be
                    run to get back a list of inputs corresponding to that function.
                'info' -> the user provided extra information about the bundled inputs

    Inputs can be specified in one of two ways:

      - The model can define `_generate_bundled_inputs_for_forward`.
        If the user chooses this method inputs should be None

      - `inputs` is a list of inputs of form List[Tuple[Any, ...]]. A list of tuples where the elements
        of each tuple are the args that make up one input.
    """
    if not isinstance(model, torch.jit.ScriptModule):
        raise Exception("Only ScriptModule is supported.")  # noqa: TRY002

    forward: Callable = model.forward

    # Sometimes forward won't have a name attached so just in case
    if not hasattr(forward, "__name__"):
        forward.__name__ = 'forward'
    augment_many_model_functions_with_bundled_inputs(
        model,
        inputs={forward : inputs},
        _receive_inflate_expr=_receive_inflate_expr,
        info={forward : info} if info else None,
        skip_size_check=skip_size_check,
    )

