
def _unlift(
    gm: torch.fx.GraphModule,
    lifted_inputs: Sequence[str | None],
    mutated_outputs: Sequence[str | None],
    in_spec: pytree.TreeSpec,
    out_spec: pytree.TreeSpec | None,
    forward_arg_names: list[str] | None = None,
):
    """
    Args:
        lifted_inputs: A list matching the graph module's input nodes. For
        an input node that is referring to a lifted parameter/buffer, this
        list will contain the fqn the corresponding attribute. Otherwise, this
        list will contain None. This is used to unlift the lifted parameters as
        get_attr nodes.

        mutated_outputs: A list matching the graph module's output nodes. For
        an output node that is referring to a mutated buffer or user input, this
        list will contain the name of the corresponding buffer or user input
        that needs to be mutated. Otherwise, this list will contain None. This
        is used to re-insert an inplace copy_ operator to copy the mutated
        values back to the original node.
    """
    unlifted_name_to_node, input_name_to_node = _unlift_inputs_as_getattr(
        gm, lifted_inputs
    )
    _insert_copy_for_mutations(
        gm, mutated_outputs, unlifted_name_to_node, input_name_to_node
    )
    gm.graph._codegen = _get_codegen(in_spec, out_spec, forward_arg_names)
    gm.graph.lint()
    gm.recompile()
    return gm

