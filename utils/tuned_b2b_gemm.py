
def tuned_b2b_gemm(
    is_left_assoc: bool,
    subgraph: Subgraph,
    A: torch._inductor.ir.TensorBox,
    B: torch._inductor.ir.TensorBox,
    C: torch._inductor.ir.TensorBox,
    *,
    layout=None,
) -> torch._inductor.ir.TensorBox:
    # call .realize() to get rid of Pointwise
    A.realize()
    B.realize()
    C.realize()
    layout = FixedLayout(
        A.get_device_or_error(),
        A.get_dtype(),
        [A.shape[0], C.shape[1]],  # type: ignore[index]
    )
    placeholders = [
        create_placeholder("inner_mm", A.get_dtype(), A.get_device_or_error())
    ]
    subgraph_buffer = build_subgraph_buffer(
        placeholders,  # type: ignore[arg-type, list-item]
        subgraph,
    )
    choices: list[TritonTemplateCaller] = []
    for config in b2b_gemm_configs:
        if is_left_assoc:
            b2b_gemm_left_template.maybe_append_choice(
                choices,
                input_nodes=(A, B, C),
                layout=layout,
                subgraphs=[subgraph_buffer],
                **config,
            )
        else:
            b2b_gemm_right_template.maybe_append_choice(
                choices,
                input_nodes=(A, B, C),
                layout=layout,
                subgraphs=[subgraph_buffer],
                **config,
            )
    # add the unoptimized choice to mitigate performance degradation
    choices.append(
        unoptimized_choice.bind(
            (A, B, C), layout, is_left_assoc=is_left_assoc, subgraph=subgraph
        )
    )
    # autotune
    node, _ = autotune_select_algorithm("b2b_gemm", choices, [A, B, C], layout)
    return node

