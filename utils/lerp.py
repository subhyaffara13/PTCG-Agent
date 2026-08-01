
def lerp(start, end, weight):
    torch._check(
        start.dtype == end.dtype,
        lambda: f"expected dtype {start.dtype} for `end`, but got dtype {end.dtype}",
    )
    args = [start, end]
    if isinstance(weight, TensorLike):
        if weight.ndim != 0:
            torch._check(
                start.dtype == weight.dtype,
                lambda: f"expected dtype {start.dtype} for `weight`, but got dtype {weight.dtype}",
            )
        args.append(weight)
    return elementwise_meta(
        *args, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )


def lerp(start: Tensor, end: Tensor, weight: Tensor | NumberType):
    inputs = [start, end]
    if isinstance(weight, Number):
        weight = start.new_full((), weight)  # type: ignore[arg-type]
    else:
        inputs.append(weight)
    if not isinstance(weight, Tensor):
        raise AssertionError(f"weight must be Tensor at this point, got {type(weight)}")
    # We implement it this way for numerical stability. We assume (in the stability optimisation)
    # that 0 <= weight <= 1. We take the abs to deal with complex numbers
    # We want to perform operations near zero, which is where floating points are most precise
    # thus, we perform the following optimisation:
    # If weight.abs() >= 0.5:
    #    return (1 - weight) * (start - end) + end
    mask = weight.abs() >= 0.5
    coeff = torch.where(mask, weight - 1, weight)
    base = torch.where(mask, end, start)
    output = coeff * (end - start) + base
    # make sure the decomposition output's stride is same as non-decomposition path.
    stride = utils.compute_elementwise_output_strides(*_maybe_broadcast(*inputs))
    if output.stride() != stride:
        output = prims.copy_strided(output, stride)

    return handle_noncontiguous_outputs(inputs, output)


def lerp(g: jit_utils.GraphContext, self, end, weight):
    # Conditional for better numeric. This has been discussed in
    # https://github.com/pytorch/pytorch/pull/18871
    diff = g.op("Sub", end, self)
    return where(
        g,
        g.op("Less", weight, g.op("Constant", value_t=torch.tensor(0.5))),
        g.op("Add", self, g.op("Mul", weight, diff)),
        g.op(
            "Sub",
            end,
            g.op(
                "Mul",
                diff,
                g.op("Sub", g.op("Constant", value_t=torch.tensor(1.0)), weight),
            ),
        ),
    )


def lerp(t, a, b):
  return optax.tree.add_scale(a, t, optax.tree.sub(b, a))

