
def bucketize(
    input: TensorBox,
    boundaries: TensorBox,
    *,
    out_int32: bool = False,
    right: bool = False,
):
    assert len(boundaries.get_size()) == 1

    if not (
        V.graph.has_feature(input, BackendFeature.BUCKETIZE)
        and V.graph.has_feature(boundaries, BackendFeature.BUCKETIZE)
    ):
        return fallback_handler(aten.bucketize.Tensor, add_to_fallback_set=False)(
            input, boundaries, out_int32=out_int32, right=right
        )

    # The entire boundaries tensor needs to be used by ops.bucketize, so we
    # need to realize it into global memory; or in other words, we can't
    # guarantee that boundaries.get_name() (used below) will exist unless
    # we call boundaries.realize().
    boundaries.realize()
    device = input.get_device()
    input_loader = input.make_loader()

    index_dtype = torch.int32 if out_int32 else torch.int64

    def inner_fn(index):
        val = input_loader(index)
        indices = ops.bucketize(
            val,
            _boundaries_helper(boundaries),
            0,
            index_dtype,
            right,
        )

        return indices

    result = Pointwise.create(
        device=device,
        dtype=index_dtype,
        inner_fn=inner_fn,
        ranges=input.get_size(),
    )

    # [NOTE: inductor bucketize realize]
    # bucketize_binary_search is relatively expensive, so we don't want to re-compute
    # it unnecessarily. If we run bucketize() and then broadcast the result, we don't
    # want this to be fused into a large number of duplicate bucketize() computations
    # for each of the elements in the result.
    #
    # If no broadcasting occurs, fusions can still occur in scheduler.py
    result.realize()

    return result


def bucketize(
    a: TensorOrNumberLikeType,
    boundaries: TensorLikeType,
    *,
    out_int32: bool = False,
    right: bool = False,
):
    torch._check(
        boundaries.dim() == 1,
        lambda: f"boundaries tensor must be 1 dimension but got dim({boundaries.dim()})",
    )

    a = a if isinstance(a, torch.Tensor) else torch.tensor(a)
    out_dtype = torch.int32 if out_int32 else torch.int64
    n_boundaries = boundaries.shape[-1]
    if n_boundaries == 0:
        return torch.zeros_like(a)
    # We are trying to find the bucket (defined by pairs of consecutive elements of `boundaries`)
    # each element of `a` belongs to. We use binary search to achieve logarithmic complexity,
    # but each step of the search is done "in parallel" over all elements of `a`
    # can't use int32 as indexes, so we have to do all computations with int64 and convert at the end
    start = torch.zeros(a.shape, device=a.device, dtype=torch.int64)
    end = start + n_boundaries
    # Max depth of the binary search
    # Since we can't break out of the loop at different points for different elements of a,
    # we just do the max amount of iterations that binary search requires and add condition
    # tensor (cond_update below) to stop updating once the search terminates

    # For first iteration through loop we can skip some checks, we have separate implementation
    mid = start + (end - start) // 2
    mid_val = boundaries[mid]
    if right:
        cond_mid = mid_val > a
    else:
        cond_mid = mid_val >= a
    start = torch.where(cond_mid, start, mid + 1)

    if n_boundaries > 1:
        cond_update = torch.ones_like(a, dtype=torch.bool)
        niters = int(math.log2(n_boundaries))
        for _ in range(niters):
            end = torch.where(cond_mid & cond_update, mid, end)
            cond_update = start < end
            # start might end up pointing to 1 past the end, we guard against that
            mid = torch.where(cond_update, start + (end - start) // 2, 0)
            mid_val = boundaries[mid]
            # If right is true, the buckets are closed on the *left*
            # (i.e., we are doing the equivalent of std::upper_bound in C++)
            # Otherwise they are closed on the right (std::lower_bound)
            if right:
                cond_mid = mid_val > a
            else:
                cond_mid = mid_val >= a
            start = torch.where((~cond_mid) & cond_update, mid + 1, start)

    return start.to(dtype=out_dtype)


def bucketize(
    g: jit_utils.GraphContext, self, boundaries, out_int32=False, right=False
):
    out_type = _C_onnx.TensorProtoDataType.INT64
    if out_int32:
        out_type = _C_onnx.TensorProtoDataType.INT32
    # A tensor expanded_boundaries is created such that it
    # contains a copy of boundaries for each element of self.
    new_shape = g.op("Concat", g.op("Shape", boundaries), g.op("Shape", self), axis_i=0)
    # Unsqueeze step is performed to respect ONNX's numpy style broadcasting for comparison ops
    # https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md
    tensor_rank = symbolic_helper._get_tensor_rank(self)
    if tensor_rank is None:
        raise AssertionError("tensor_rank must be non-None")
    unsqueeze_axes = list(range(1, tensor_rank + 1))
    expanded_boundaries = expand(
        g,
        symbolic_helper._unsqueeze_helper(g, boundaries, unsqueeze_axes),
        new_shape,
        None,
    )
    # Compare each element of self to boundaries to get a tensor
    # with leading 1s and trailing 0s.
    # e.g., 4 > [1, 3, 4] = [1, 1, 0]
    # The index of the last 1 is the bucket where the element should go.
    if right:
        cond = ge(g, self, expanded_boundaries)
    else:
        cond = gt(g, self, expanded_boundaries)
    cond_out = g.op("Cast", cond, to_i=out_type)
    # Sum to get the number of 1s corresponding to each element,
    # which is the same as the bucket index.
    # e.g., sum(4 > [1, 3, 4]) = sum([1, 1, 0]) = 2
    return symbolic_helper._reducesum_helper(g, cond_out, axes_i=[0], keepdims_i=0)

