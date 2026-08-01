
def test_torch_array_operations():
    if not torch:
        skip("PyTorch not installed")

    M = MatrixSymbol("M", 2, 2)
    N = MatrixSymbol("N", 2, 2)
    P = MatrixSymbol("P", 2, 2)
    Q = MatrixSymbol("Q", 2, 2)

    ma = torch.tensor([[1., 2.], [3., 4.]], dtype=torch.float64)
    mb = torch.tensor([[1., -2.], [-1., 3.]], dtype=torch.float64)
    mc = torch.tensor([[2., 0.], [1., 2.]], dtype=torch.float64)
    md = torch.tensor([[1., -1.], [4., 7.]], dtype=torch.float64)

    cg = ArrayTensorProduct(M, N)
    assert torch_code(cg) == 'torch.einsum("ab,cd", M, N)'
    f = lambdify((M, N), cg, 'torch')
    y = f(ma, mb)
    c = torch.einsum("ij,kl", ma, mb)
    assert torch.allclose(y, c)

    cg = ArrayAdd(M, N)
    assert torch_code(cg) == 'torch.add(M, N)'
    f = lambdify((M, N), cg, 'torch')
    y = f(ma, mb)
    c = ma + mb
    assert torch.allclose(y, c)

    cg = ArrayAdd(M, N, P)
    assert torch_code(cg) == 'torch.add(torch.add(M, N), P)'
    f = lambdify((M, N, P), cg, 'torch')
    y = f(ma, mb, mc)
    c = ma + mb + mc
    assert torch.allclose(y, c)

    cg = ArrayAdd(M, N, P, Q)
    assert torch_code(cg) == 'torch.add(torch.add(torch.add(M, N), P), Q)'
    f = lambdify((M, N, P, Q), cg, 'torch')
    y = f(ma, mb, mc, md)
    c = ma + mb + mc + md
    assert torch.allclose(y, c)

    cg = PermuteDims(M, [1, 0])
    assert torch_code(cg) == 'M.permute(1, 0)'
    f = lambdify((M,), cg, 'torch')
    y = f(ma)
    c = ma.T
    assert torch.allclose(y, c)

    cg = PermuteDims(ArrayTensorProduct(M, N), [1, 2, 3, 0])
    assert torch_code(cg) == 'torch.einsum("ab,cd", M, N).permute(1, 2, 3, 0)'
    f = lambdify((M, N), cg, 'torch')
    y = f(ma, mb)
    c = torch.einsum("ab,cd", ma, mb).permute(1, 2, 3, 0)
    assert torch.allclose(y, c)

    cg = ArrayDiagonal(ArrayTensorProduct(M, N), (1, 2))
    assert torch_code(cg) == 'torch.einsum("ab,bc->acb", M, N)'
    f = lambdify((M, N), cg, 'torch')
    y = f(ma, mb)
    c = torch.einsum("ab,bc->acb", ma, mb)
    assert torch.allclose(y, c)

