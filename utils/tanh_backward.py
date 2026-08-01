
def tanh_backward(out_grad: Tensor, y: Tensor):
    return out_grad * (1 - y * y).conj_physical()


def tanh_backward(out_grad: ComplexTensor, y: ComplexTensor) -> ComplexTensor:
    # pyrefly: ignore[bad-return]
    return out_grad * (1.0 - y * y).conj_physical()

