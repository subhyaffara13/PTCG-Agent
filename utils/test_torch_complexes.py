
def test_torch_complexes():
    assert torch_code(re(x)) == "torch.real(x)"
    assert torch_code(im(x)) == "torch.imag(x)"
    assert torch_code(arg(x)) == "torch.angle(x)"

