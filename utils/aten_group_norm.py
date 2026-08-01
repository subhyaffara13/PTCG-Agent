
def aten_group_norm(
    input: TFloat,
    num_groups: int,
    weight: TFloat | None = None,
    bias: TFloat | None = None,
    eps: float = 1e-05,
    cudnn_enabled: bool = True,
) -> TFloat:
    """group_norm(Tensor input, int num_groups, Tensor? weight=None, Tensor? bias=None, float eps=1e-05, bool cudnn_enabled=True) -> Tensor"""

    c = op21.Shape(input, start=1, end=2)
    if weight is None:
        weight = op21.ConstantOfShape(c, value=ir.tensor([1.0], dtype=input.dtype))
    if bias is None:
        bias = op21.ConstantOfShape(c, value=ir.tensor([0.0], dtype=input.dtype))
    return op21.GroupNormalization(
        input, weight, bias, epsilon=eps, num_groups=num_groups
    )

