
def get_size_hints(mat1, mat2, m, n, k):
    if not isinstance(m, int) or not isinstance(k, int):
        (m, k) = V.graph.sizevars.optimization_hints(mat1.get_size())

    if not isinstance(n, int) or not isinstance(k, int):
        (k, n) = V.graph.sizevars.optimization_hints(mat2.get_size())
    return m, n, k

