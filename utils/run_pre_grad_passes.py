
def run_pre_grad_passes(
    model_: GraphModule, example_inputs_: Sequence[InputType]
) -> GraphModule:
    # "before_pre_grad_graph" is used in inductor provenance
    # tracking highlighter front-end.
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "before_pre_grad_graph",
            "encoding": "string",
        },
        payload_fn=lambda: model_.print_readable(
            print_output=False, include_stride=True, include_device=True
        )
        + f"\n\n # graph id: {id(model_.graph)}",
    )
    pre_grad_graphs_log.debug(
        "%s",
        lazy_format_graph_code(
            "BEFORE PRE GRAD",
            model_,
            include_stride=True,
            include_device=True,
            colored=True,
        ),
    )
    torch._inductor.debug._pre_grad_graph_id = id(model_.graph)

    if config.trace.provenance_tracking_level == 1:
        for node in model_.graph.nodes:
            if node.stack_trace:
                torch._inductor.debug._inductor_pre_grad_node_stack_trace[node.name] = (
                    node.stack_trace
                )

    model_ = _recursive_pre_grad_passes(model_, example_inputs_)
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "after_pre_grad_graph",
            "encoding": "string",
        },
        payload_fn=lambda: model_.print_readable(
            print_output=False, include_stride=True, include_device=True
        )
        + f"\n\n # graph id: {id(model_.graph)}",
    )
    return model_

