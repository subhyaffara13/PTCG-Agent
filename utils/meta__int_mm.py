
def meta__int_mm(a, b):
    torch._check(a.dim() == 2, lambda: "a must be a 2D tensor")
    torch._check(b.dim() == 2, lambda: "b must be a 2D tensor")
    torch._check(
        a.dtype in [torch.int8, torch.uint8],
        lambda: f"expected self to be int8 or uint8, got {a.dtype}",
    )
    torch._check(
        b.dtype is torch.int8,
        lambda: f"expected mat2 to be int8, got {b.dtype}",
    )
    torch._check(
        a.size(1) == b.size(0),
        lambda: (
            f"Incompatible matrix sizes for _int_mm ({a.size(0)}x{a.size(1)} "
            f"and {b.size(0)}x{b.size(1)})"
        ),
    )
    return a.new_empty((a.size(0), b.size(1)), dtype=torch.int32)

