from typing import Any, Callable

def fn_input_mutations_to_outputs(
    fn: Callable[..., Any],
    args_descs: list[AOTInput],
    meta: ViewAndMutationMeta,
    keep_data_input_mutations: bool,
) -> Any:
    @simple_wraps(fn)
    def inner_fn(*args: FxValue) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
        outs, outs_descs = call_and_expect_output_descs(fn, args)
        if len(meta.output_info) != len(outs):
            raise AssertionError(
                f"output_info length ({len(meta.output_info)}) != outs length ({len(outs)})"
            )
        # The compiled fw will return mutated input tensors, *including* metadata-only mutation.
        # However, if keep_data_input_mutations is set, the compiled fw only needs to return metadata-mutated inputs.
        # (because data-only input mutations are handled directly in the compiled graph)
        mutated_input_pairs = [
            (x, InputMutationAOTOutput(src))
            for (i, (x, src)) in enumerate(zip(args, args_descs))
            if i in meta.mutated_inp_runtime_indices
        ]
        if mutated_input_pairs:
            mutated_inputs_to_return, mutated_inputs_to_return_descs = zip(
                *mutated_input_pairs
            )
        else:
            mutated_inputs_to_return, mutated_inputs_to_return_descs = (), ()
        return (
            (*mutated_inputs_to_return, *outs),
            (*mutated_inputs_to_return_descs, *outs_descs),
        )

    return inner_fn

