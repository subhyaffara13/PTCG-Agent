
def test_torch_complex_operations():
    if not torch:
        skip("PyTorch not installed")

    expr = conjugate(x)
    assert torch_code(expr) == "torch.conj(x)"

    # SymPy distributes conjugate over addition and applies specific rules for each term
    expr = conjugate(sin(x) + I * cos(y))
    assert torch_code(expr) == "torch.sin(torch.conj(x)) - 1j*torch.cos(torch.conj(y))"

    expr = I
    assert torch_code(expr) == "1j"

    expr = 2 * I + x
    assert torch_code(expr) == "x + 2*1j"

    expr = exp(I * x)
    assert torch_code(expr) == "torch.exp(1j*x)"

