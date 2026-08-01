
def rewrite_signature(
    f_sig: inspect.Signature,
    graph: torch.fx.GraphModule,
    fake_mode: fake_tensor.FakeTensorMode | None,
    flat_args: list[Any],
    in_spec: pytree.TreeSpec,
    example_fake_inputs: list[Any],
    graph_captured_input: Iterable[Any],
    graph_captured_output: Iterable[Any] | None,
    dynamo_traced_result: Any,
    flat_args_dynamic_dims: list[set[int]],
) -> torch.fx.GraphModule:
    orig_args, orig_kwargs = pytree.tree_unflatten(flat_args, in_spec)

    check_user_input_output(flat_args, UserErrorType.INVALID_INPUT)
    flat_results_traced, out_spec_traced = pytree.tree_flatten(dynamo_traced_result)
    check_user_input_output(flat_results_traced, UserErrorType.INVALID_OUTPUT)

    def check_optional_input_and_error(f_sig: inspect.Signature) -> None:
        # Check if function has optional input.
        for name, param in f_sig.parameters.items():
            if param.default is not inspect.Parameter.empty:
                import torch._dynamo.graph_break_hints as graph_break_hints
                from torch._dynamo.exc import unimplemented

                log.error(
                    "Parameter %s is optional with a default value of %s",
                    name,
                    param.default,
                )
                unimplemented(
                    gb_type="rewrite_signature: cannot trace optional function input",
                    context="",
                    explanation=f"Parameter {name} is optional with a default value of {param.default}. This is not supported yet.",
                    hints=[
                        *graph_break_hints.SUPPORTABLE,
                    ],
                )

    def produce_matching(
        debug_type: str, sources: Iterable[Any], candidates: Iterable[Any]
    ) -> list[int | None]:
        matched_elements_positions: list[int | None] = []
        dict_of_source_vals = {}
        for i, val in enumerate(sources):
            dict_of_source_vals[id(val)] = i

        for val in candidates:
            if isinstance(val, tuple(common_constant_types)):
                matched_elements_positions.append(None)
            elif id(val) not in dict_of_source_vals:
                if debug_type == "inputs":
                    check_optional_input_and_error(f_sig)
                raise AssertionError(
                    f"Unexpectedly found a {type(val)} in the {debug_type}.\n"
                    'Please file an issue along with a paste of the logs from TORCH_LOGS="+export"',
                )
            else:
                matched_elements_positions.append(dict_of_source_vals[id(val)])

        return matched_elements_positions

    matched_input_elements_positions = produce_matching(
        "inputs", flat_args, graph_captured_input
    )

    assert graph_captured_output is not None
    matched_output_elements_positions = produce_matching(
        "outputs", list(graph_captured_output) + flat_args, flat_results_traced
    )

    new_graph = FlattenInputOutputSignature(
        graph,
        flat_args,
        matched_input_elements_positions,  # type: ignore[arg-type]
        flat_results_traced,
        matched_output_elements_positions,  # type: ignore[arg-type]
        example_fake_inputs,
        flat_args_dynamic_dims,
        fake_mode,
    ).transform()

    new_graph.graph._codegen = _PyTreeCodeGen(
        _PyTreeInfo(
            argument_names(f_sig, orig_args, orig_kwargs),
            in_spec,
            out_spec_traced,
        )
    )
    new_graph.recompile()
    return new_graph

