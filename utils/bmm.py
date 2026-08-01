
def bmm(self: list[int], mat2: list[int]) -> list[int]:
    if len(self) != 3:
        raise AssertionError(f"bmm only supports 3D tensors, got {len(self)}D")
    if len(mat2) != 3:
        raise AssertionError(f"bmm only supports 3D tensors, got {len(mat2)}D")
    if self[0] != mat2[0]:
        raise AssertionError(
            f"mismatching batch dimension: self[0]={self[0]}, mat2[0]={mat2[0]}"
        )
    if self[2] != mat2[1]:
        raise AssertionError(
            f"mismatching contracting dimension: self[2]={self[2]}, mat2[1]={mat2[1]}"
        )
    return [self[0], self[1], mat2[2]]


def bmm(
    self: torch.Tensor,
    batch2: torch.Tensor,
    out_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    # Outer-product specialization: [B, M, 1] x [B, 1, N] -> [B, M, N].
    # This avoids introducing a reduction and maps directly to broadcasted mul.
    if statically_known_true(self.shape[2] == 1) or statically_known_true(
        batch2.shape[1] == 1
    ):
        return (self * batch2).contiguous()

    # TODO: Re-enable for mps once our reductions are performant enough
    # (https://github.com/pytorch/pytorch/issues/150121)
    if config.coordinate_descent_tuning and self.device.type not in ["cpu", "mps"]:
        if statically_known_true(self.shape[1] == 1) or statically_known_true(
            batch2.shape[2] == 1
        ):
            out = (self.unsqueeze(-1) * batch2.unsqueeze(1)).sum(dim=2)
            return out
    if self.device.type == "cpu":
        if statically_known_true(self.size(1) == 1) and statically_known_true(
            batch2.size(-1) == 1
        ):
            counters["inductor"]["decompose_bmm"] += 1
            return torch.sum(
                self.squeeze(1) * batch2.squeeze(-1), dim=1, keepdim=True
            ).unsqueeze(1)
    return NotImplemented


def bmm(g: jit_utils.GraphContext, self, other):
    if symbolic_helper._try_get_scalar_type(self):
        old_type, self, other = _try_cast_integer_to_float(g, self, other)
        return _cast_to_type(g, g.op("MatMul", self, other), old_type)
    else:
        return g.op("MatMul", self, other)


def bmm(g: jit_utils.GraphContext, self, other):
    return g.op("MatMul", self, other)

