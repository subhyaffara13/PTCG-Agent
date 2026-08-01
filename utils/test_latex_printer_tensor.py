
def test_latex_printer_tensor():
    from sympy.tensor.tensor import TensorIndexType, tensor_indices, TensorHead, tensor_heads
    L = TensorIndexType("L")
    i, j, k, l = tensor_indices("i j k l", L)
    i0 = tensor_indices("i_0", L)
    A, B, C, D = tensor_heads("A B C D", [L])
    H = TensorHead("H", [L, L])
    K = TensorHead("K", [L, L, L, L])

    assert latex(i) == r"{}^{i}"
    assert latex(-i) == r"{}_{i}"

    expr = A(i)
    assert latex(expr) == r"A{}^{i}"

    expr = A(i0)
    assert latex(expr) == r"A{}^{i_{0}}"

    expr = A(-i)
    assert latex(expr) == r"A{}_{i}"

    expr = -3*A(i)
    assert latex(expr) == r"-3A{}^{i}"

    expr = K(i, j, -k, -i0)
    assert latex(expr) == r"K{}^{ij}{}_{ki_{0}}"

    expr = K(i, -j, -k, i0)
    assert latex(expr) == r"K{}^{i}{}_{jk}{}^{i_{0}}"

    expr = K(i, -j, k, -i0)
    assert latex(expr) == r"K{}^{i}{}_{j}{}^{k}{}_{i_{0}}"

    expr = H(i, -j)
    assert latex(expr) == r"H{}^{i}{}_{j}"

    expr = H(i, j)
    assert latex(expr) == r"H{}^{ij}"

    expr = H(-i, -j)
    assert latex(expr) == r"H{}_{ij}"

    expr = (1+x)*A(i)
    assert latex(expr) == r"\left(x + 1\right)A{}^{i}"

    expr = H(i, -i)
    assert latex(expr) == r"H{}^{L_{0}}{}_{L_{0}}"

    expr = H(i, -j)*A(j)*B(k)
    assert latex(expr) == r"H{}^{i}{}_{L_{0}}A{}^{L_{0}}B{}^{k}"

    expr = A(i) + 3*B(i)
    assert latex(expr) == r"3B{}^{i} + A{}^{i}"

    # Test ``TensorElement``:
    from sympy.tensor.tensor import TensorElement

    expr = TensorElement(K(i, j, k, l), {i: 3, k: 2})
    assert latex(expr) == r'K{}^{i=3,j,k=2,l}'

    expr = TensorElement(K(i, j, k, l), {i: 3})
    assert latex(expr) == r'K{}^{i=3,jkl}'

    expr = TensorElement(K(i, -j, k, l), {i: 3, k: 2})
    assert latex(expr) == r'K{}^{i=3}{}_{j}{}^{k=2,l}'

    expr = TensorElement(K(i, -j, k, -l), {i: 3, k: 2})
    assert latex(expr) == r'K{}^{i=3}{}_{j}{}^{k=2}{}_{l}'

    expr = TensorElement(K(i, j, -k, -l), {i: 3, -k: 2})
    assert latex(expr) == r'K{}^{i=3,j}{}_{k=2,l}'

    expr = TensorElement(K(i, j, -k, -l), {i: 3})
    assert latex(expr) == r'K{}^{i=3,j}{}_{kl}'

    expr = PartialDerivative(A(i), A(i))
    assert latex(expr) == r"\frac{\partial}{\partial {A{}^{L_{0}}}}{A{}^{L_{0}}}"

    expr = PartialDerivative(A(-i), A(-j))
    assert latex(expr) == r"\frac{\partial}{\partial {A{}_{j}}}{A{}_{i}}"

    expr = PartialDerivative(K(i, j, -k, -l), A(m), A(-n))
    assert latex(expr) == r"\frac{\partial^{2}}{\partial {A{}^{m}} \partial {A{}_{n}}}{K{}^{ij}{}_{kl}}"

    expr = PartialDerivative(B(-i) + A(-i), A(-j), A(-n))
    assert latex(expr) == r"\frac{\partial^{2}}{\partial {A{}_{j}} \partial {A{}_{n}}}{\left(A{}_{i} + B{}_{i}\right)}"

    expr = PartialDerivative(3*A(-i), A(-j), A(-n))
    assert latex(expr) == r"\frac{\partial^{2}}{\partial {A{}_{j}} \partial {A{}_{n}}}{\left(3A{}_{i}\right)}"

