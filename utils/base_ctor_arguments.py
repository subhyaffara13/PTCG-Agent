
def base_ctor_arguments(func: FunctionSchema) -> list[Binding]:
    # All specializations are parematerized by `has_symbolic_inputs` flag.
    arguments = [has_symbolic_inputs_binding]

    # If `func` might return more than 1 value, we also parameterize this specialization
    # with the output index.
    if is_multi_output(func):
        arguments.append(out_index_binding)

    return arguments

