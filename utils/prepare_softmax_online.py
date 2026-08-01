
def prepare_softmax_online(x, dim):
    """
    Lowering inductor_prims.prepare_softmax_online to compute max/sum in one pass if no split is needed.
    """
    kwargs = _make_reduction_inner(
        x, axis=dim, keepdims=True, dtype=None, override_return_dtype=None
    )

    reduction_ranges = kwargs["reduction_ranges"]
    rnumel = V.graph.sizevars.simplify(sympy_product(reduction_ranges))
    hint, num_split = ir.Reduction.num_splits(
        **kwargs,
        reduction_type="online_softmax_reduce",  # type: ignore[arg-type]
        reduction_numel=rnumel,
    )

    if num_split == 1 and V.graph.sizevars.statically_known_geq(
        rnumel, config.unroll_reductions_threshold
    ):
        max_tensor, sum_tensor = OnlineSoftmaxReduction.create(
            input_node=x, num_output=2, reduction_hint=hint, **kwargs
        )
        return max_tensor, sum_tensor
    else:
        # Note: [Split online_softmax_reduce]
        # We don't split reduction for online_softmax_reduce for now.
        # On one hand, supporting split reduction makes things complex since
        # the split out reuctions requires 2 inputs rather than one.
        # On the other hand, during training the online_softmax_reduce should
        # usually don't requires a split due to large batch size
        # (more specifically batch size times sequence length).
        # We should support split reduction if we find legit use cases to
        # motivate the work.
        #
        # TODO: does inference need split online_softmax_reduce?

        log.debug(
            "Online softmax is disabled on the fly since Inductor decides to split the reduction."
        )
        amax = reduce_amax(x, dim, keepdims=True)
        exp = lowerings[aten.exp](sub(x, amax))
        xsum = sum_(exp, dim, keepdims=True)
        return amax, xsum

