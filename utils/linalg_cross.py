
def linalg_cross(self, other, *, dim=-1):
    x_d = self.ndim
    y_d = other.ndim
    torch._check(
        x_d == y_d,
        lambda: "linalg.cross: inputs must have the same number of dimensions.",
    )
    torch._check(
        self.size(dim) == 3 and other.size(dim) == 3,
        lambda: (
            f"linalg.cross: inputs dimension {dim} must have length 3. "
            f"Got {self.size(dim)} and {other.size(dim)}"
        ),
    )
    out_shape = _broadcast_shapes(self.shape, other.shape)
    return self.new_empty(out_shape)


def linalg_cross(g: jit_utils.GraphContext, input, other, dim=-1):
    return cross(g, input, other, dim)

