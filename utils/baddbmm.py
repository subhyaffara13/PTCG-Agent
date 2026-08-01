
def baddbmm(self, batch1, batch2, beta=1, alpha=1):
    if not self.is_floating_point() and not self.is_complex():
        beta = int(beta)
        alpha = int(alpha)
    result = torch.bmm(batch1, batch2)
    if not isinstance(alpha, numbers.Number) or alpha != 1:
        result = result * alpha
    if beta == 0:
        return result
    if not isinstance(beta, numbers.Number) or beta != 1:
        self = self * beta
    return self + result


def baddbmm(g: jit_utils.GraphContext, self, batch1, batch2, beta, alpha):
    scalar_type = _type_utils.JitScalarType.from_value(self)
    batch_mul = matmul(g, batch1, batch2)
    mul_a = mul(
        g,
        batch_mul,
        g.op("Cast", alpha, to_i=scalar_type.onnx_type()),
    )
    mul_b = mul(
        g,
        self,
        g.op("Cast", beta, to_i=scalar_type.onnx_type()),
    )
    return add(g, mul_a, mul_b)

