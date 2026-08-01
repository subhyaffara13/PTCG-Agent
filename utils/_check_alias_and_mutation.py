
def _check_alias_and_mutation(graph_module, inputs_fake, name, pre_dispatch):
    aliases, inp_mutation = has_potential_input_alias_or_mutation(
        graph_module, inputs_fake, pre_dispatch=pre_dispatch
    )
    if aliases:
        raise RuntimeError(f"{name} might be aliasing the input or the output!")  # noqa: F541
    if inp_mutation:
        raise RuntimeError(f"{name} might be modifying the input!")  # noqa: F541

