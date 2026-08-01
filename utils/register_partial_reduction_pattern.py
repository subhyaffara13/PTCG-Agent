
def register_partial_reduction_pattern():
    "Reuse partial reductions in complete reductions"

    # post grad equivalents
    equiv_red = {
        aten.amax.default: aten.max.default,
        aten.amin.default: aten.min.default,
    }

    # TODO: to support other reductions like sum, would need to skip
    # lower precision reductions since partial output would need to be kept at fp32.
    for red_op in (aten.amax.default, aten.amin.default):
        inp = KeywordArg("input")
        partial_reduc = CallFunction(
            red_op, inp, KeywordArg("reduced_dims"), KeywordArg("keepdim")
        )
        full_reduc = CallFunction([red_op, equiv_red[red_op]], inp)

        @register_graph_pattern(
            MultiOutputPattern([partial_reduc, full_reduc]),
            # pyrefly: ignore [bad-argument-type]
            pass_dict=pass_patterns[2],
        )
        def reuse_partial(match, input, reduced_dims, keepdim):
            partial_red, full_red = match.output_nodes()

            # if they're small, reuse not worth it
            if not statically_known_true(input.meta["val"].numel() >= 4096):
                return True

            def replacement(inp: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
                partial = partial_red.target(inp, reduced_dims, keepdim)
                complete = full_red.target(partial)
                return (partial, complete)

            counters["inductor"]["partial_reduction_reuse"] += 1
            match.replace_by_example(replacement, [input])

