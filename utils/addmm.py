
def addmm(self: list[int], mat1: list[int], mat2: list[int], beta: Any, alpha: Any):
    return broadcast(self, mm(mat1, mat2))


def addmm(self: Tensor, mat1: Tensor, mat2: Tensor, beta: int = 1, alpha: int = 1):
    if not self.is_floating_point() and not self.is_complex():
        beta = int(beta)
        alpha = int(alpha)
    out = alpha * torch.mm(mat1, mat2)
    if beta == 0:
        return out

    # The output of aten.addmm is contiguous, we need to match this behavior in the decomposition.
    # The original implementation 'beta * self + out' would return a strided tensor if `self` is strided.
    # We thus use `out`, the output of torch.mm, which is always contiguous, as the first argument for addition.
    # This is relying on TensorIterator's behavior that it takes higher precedence on the stride of first input.
    # Alternative, we can write `(beta * self + out).contiguous()`, but it introduces another copy in some cases.
    # This implementation is not ideal, and we should revisit this when we have a better solution.
    return out + beta * self


def addmm(
    self: torch.Tensor,
    mat1: torch.Tensor,
    mat2: torch.Tensor,
    out_dtype: torch.dtype | None = None,
    beta: torch.types.Number = 1,
    alpha: torch.types.Number = 1,
) -> torch.Tensor:
    if mat1.device.type not in ["cpu", "mps"]:
        if (
            statically_known_true(mat1.size(-1) == 1)
            and statically_known_true(mat1.size(0) != 1)
            and statically_known_true(mat2.size(1) != 1)
        ):
            counters["inductor"]["decompose_addmm"] += 1
            out = mat1 * mat2
            return alpha * out + beta * self

    if self.device.type == "cpu":
        if statically_known_true(mat1.size(0) == 1) and statically_known_true(
            mat2.size(-1) == 1
        ):
            counters["inductor"]["decompose_addmm"] += 1
            out = torch.sum(
                mat1.squeeze(0) * mat2.squeeze(-1), dim=0, keepdim=True
            ).unsqueeze(0)
            return alpha * out + beta * self
        if (
            statically_known_true(mat1.size(0) == 1)
            and guard_or_false(mat2.size(0) <= 16)
            and guard_or_false(mat2.size(1) <= 16)
        ):
            counters["inductor"]["decompose_addmm"] += 1
            out = (mat1.T * mat2).sum(dim=0, keepdim=True)
            return alpha * out + beta * self
    return NotImplemented


def addmm(match, mat1, mat2, *, inp):
    def repl(inp, mat1, mat2):
        return aten.addmm(inp, mat1, mat2)

    match.replace_by_example(repl, [inp, mat1, mat2])


def addmm(g: jit_utils.GraphContext, self, mat1, mat2, beta, alpha):
    if symbolic_helper._try_get_scalar_type(self):
        old_type, self, mat1, mat2 = _try_cast_integer_to_float(g, self, mat1, mat2)
        return _cast_to_type(
            g,
            g.op(
                "Gemm",
                mat1,
                mat2,
                self,
                beta_f=symbolic_helper._scalar(beta),
                alpha_f=symbolic_helper._scalar(alpha),
            ),
            old_type,
        )
    else:
        return g.op(
            "Gemm",
            mat1,
            mat2,
            self,
            beta_f=symbolic_helper._scalar(beta),
            alpha_f=symbolic_helper._scalar(alpha),
        )


def addmm(g: jit_utils.GraphContext, self, mat1, mat2, beta, alpha):
    scalar_type = None
    self_scalar_type = symbolic_helper._try_get_scalar_type(self)
    mat1_scalar_type = symbolic_helper._try_get_scalar_type(mat1)
    mat2_scalar_type = symbolic_helper._try_get_scalar_type(mat2)
    if self_scalar_type is not None:
        scalar_type = self_scalar_type
    elif mat1_scalar_type is not None:
        scalar_type = mat1_scalar_type
    elif mat2_scalar_type is not None:
        scalar_type = mat2_scalar_type

    mat1_rank = symbolic_helper._get_tensor_rank(mat1)
    mat2_rank = symbolic_helper._get_tensor_rank(mat2)

    def is_not_none_nor(v, u):
        return v is not None and v != u

    if scalar_type is not None and (
        is_not_none_nor(mat1_rank, 2) or is_not_none_nor(mat2_rank, 2)
    ):
        res1 = g.op("MatMul", mat1, mat2)
        res2 = self

        alpha = symbolic_helper._scalar(alpha)
        beta = symbolic_helper._scalar(beta)

        if alpha != 1:
            alpha = g.op(
                "Constant", value_t=torch.tensor(alpha, dtype=scalar_type.dtype())
            )
            res1 = g.op("Mul", res1, alpha)
        if beta != 1:
            beta = g.op(
                "Constant",
                value_t=torch.tensor(
                    symbolic_helper._scalar(beta), dtype=scalar_type.dtype()
                ),
            )
            res2 = g.op("Mul", res2, beta)

        return g.op("Add", res1, res2)

    return g.op(
        "Gemm",
        mat1,
        mat2,
        self,
        beta_f=symbolic_helper._scalar(beta),
        alpha_f=symbolic_helper._scalar(alpha),
    )

