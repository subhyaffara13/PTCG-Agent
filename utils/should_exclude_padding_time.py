
def should_exclude_padding_time(match: Match, arg_name: str) -> bool:
    from torch._prims_common import is_contiguous_or_false

    node_def = get_non_view_def(match.kwargs[arg_name])

    # constant padding converts tensors to contiguous so even if the input tensor
    # can be planned layout transform is not free. TODO - way to pad and preserve layout ?
    # Use is_contiguous_or_false to avoid guarding on data-dependent expressions
    # with unbacked symints - returns False instead of raising an error.
    if not is_contiguous_or_false(fetch_fake_tensors(match, (arg_name,))[0]):
        return False

    # TODO - see issue https://github.com/pytorch/pytorch/issues/128889
    # We would only able to completely plan these out if we were only doing
    # first dimension padding. non-first we would still need a copy
    # because these outputs are fixed dense.
    cannot_plan_output = [
        aten.mm.default,
        aten.convolution.default,
        aten.convolution_backward.default,
        aten.bmm.default,
        aten.addmm.default,
        aten._scaled_dot_product_flash_attention.default,
        aten._scaled_dot_product_efficient_attention.default,
    ]

    if node_def.target in cannot_plan_output:
        return False

    if (
        node_def.target is aten.cat.default
        and len(node_def.all_input_nodes)
        > torch._inductor.config.max_pointwise_cat_inputs
    ):
        return False

    # optimistically assume we should be able to memory plan away
    # all non inputs
    return node_def.op != "placeholder"

