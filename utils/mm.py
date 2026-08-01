
def mm(self: list[int], mat2: list[int]):
    if len(self) != 2:
        raise AssertionError(f"self must be a matrix (got {len(self)} dimensions)")
    if len(mat2) != 2:
        raise AssertionError(f"mat2 must be a matrix (got {len(mat2)} dimensions)")

    if self[1] != mat2[0]:
        raise AssertionError(
            f"Matrix dimensions don't match for mm: self[1]={self[1]}, mat2[0]={mat2[0]}"
        )
    return [self[0], mat2[1]]


def mm(
    self: torch.Tensor,
    input2: torch.Tensor,
    out_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    # Our matrix vector multiplies only achieve peak bandwidth with coordinate descent tuning.
    # todo: Look into why and fix it (hopefully)

    # TODO: Re-enable for mps once our reductions are performant enough
    # (https://github.com/pytorch/pytorch/issues/150121)
    if config.coordinate_descent_tuning and self.device.type not in ["cpu", "mps"]:
        if statically_known_true(self.shape[0] == 1) or statically_known_true(
            input2.shape[1] == 1
        ):
            return (self.unsqueeze(2) * input2.unsqueeze(0)).sum(dim=1)
    # Non-CPU/MPS: always decompose. CPU: only for small tensors.
    if (
        statically_known_true(self.size(-1) == 1)
        and statically_known_true(self.size(0) != 1)
        and statically_known_true(input2.size(1) != 1)
    ):
        if self.device.type not in ["cpu", "mps"] or (
            self.device.type == "cpu"
            and statically_known_true(self.size(0) > 0)
            and statically_known_true(input2.size(0) == 1)
            and (self.dtype == input2.dtype)
            and guard_or_false((torch.numel(self) + torch.numel(input2)) <= 32)
        ):
            counters["inductor"]["decompose_mm"] += 1
            return self * input2
    if self.device.type == "cpu":
        if statically_known_true(self.size(0) == 1) and statically_known_true(
            input2.size(-1) == 1
        ):
            counters["inductor"]["decompose_mm"] += 1
            return torch.sum(
                self.squeeze(0) * input2.squeeze(-1), dim=0, keepdim=True
            ).unsqueeze(0)
    return NotImplemented


def mm(g: jit_utils.GraphContext, self, other):
    return g.op("Gemm", self, other, beta_f=0.0, alpha_f=1.0)


def mm(g: jit_utils.GraphContext, self, other):
    # Create a dummy C tensor. Only needed for API purposes, the value is
    # since beta = 0
    scalar_type = symbolic_helper._try_get_scalar_type(self, other)
    if scalar_type is None:
        raise errors.SymbolicValueError(
            "mm can only operate on tensors with known types", self
        )
    zero_constant = g.op(
        "Constant",
        value_t=torch.tensor([0], dtype=scalar_type.dtype()),
    )

    if symbolic_helper._try_get_scalar_type(self):
        old_type, self, other, zero_constant = _try_cast_integer_to_float(
            g, self, other, zero_constant
        )
        return _cast_to_type(
            g,
            g.op("Gemm", self, other, zero_constant, beta_f=0.0, alpha_f=1.0),
            old_type,
        )
    return g.op("Gemm", self, other, zero_constant, beta_f=0.0, alpha_f=1.0)


def mm(g: jit_utils.GraphContext, self, other):
    # Create a dummy C tensor. Only needed for API purposes, the value is
    # since beta = 0
    C = g.op("Constant", value_t=torch.tensor([1]))
    return g.op("Gemm", self, other, C, beta_f=0.0, alpha_f=1.0)

