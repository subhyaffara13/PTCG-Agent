
def mv(self: list[int], vec: list[int]):
    if not (len(self) == 2 and len(vec) == 1):
        raise AssertionError(
            f"Expected 2D matrix and 1D vector, got len(self)={len(self)}, "
            f"len(vec)={len(vec)}"
        )
    if self[1] != vec[0]:
        raise AssertionError(
            f"Matrix-vector dimension mismatch: self[1]={self[1]}, vec[0]={vec[0]}"
        )
    # TODO: return self
    return [self[0]]


def mv(self, vec):
    torch._check(
        self.dim() == 2 and vec.dim() == 1,
        lambda: f"matrix @ vector expected, got {self.dim()}, {vec.dim()}",
    )
    torch._check(
        self.size(1) == vec.size(0),
        lambda: f"size mismatch, got input ({self.size(0)}x{self.size(1)}), vec ({vec.size(0)})",
    )
    return (self * vec).sum(dim=1)


def mv(g: jit_utils.GraphContext, self, vec):
    return matmul(g, self, vec)

