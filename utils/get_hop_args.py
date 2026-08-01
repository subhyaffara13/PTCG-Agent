
def get_hop_args(
    tx: "InstructionTranslator",
    f: VariableTracker,
    subtracer: "SubgraphTracer",
    sub_args: list[VariableTracker],
    sub_kwargs: dict[str, VariableTracker],
    set_subgraph_inputs: str,
    description: str,
) -> list[VariableTracker]:
    sub_args_names = maybe_positional_arg_names(f)
    # User mismatch in the number of args. Will eventually lead to an error.
    if sub_args_names is not None and len(sub_args_names) < len(sub_args):
        sub_args_names = None
    args = validate_args_and_maybe_create_graph_inputs(
        sub_args,
        subtracer,
        tx,
        set_subgraph_inputs,
        description,
        sub_args_names,
    )

    validate_args_and_maybe_create_graph_inputs(
        sub_kwargs.values(),  # type: ignore[arg-type]
        subtracer,
        tx,
        set_subgraph_inputs="automatic",
        description=description,
    )
    return args

