
def sample_inputs_einsum(op_info, device, dtype, requires_grad=False, **kwargs):
    def c(t):
        return t.clone().requires_grad_(requires_grad)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    x = make_arg((3,))
    y = make_arg((4,))
    A = make_arg((2, 3,))
    B = make_arg((1, 3,))
    C = make_arg((1, 2, 3,))
    D = make_arg((1, 3, 4,))
    E = make_arg((4, 4,))
    H = make_arg((3, 3,))
    I = make_arg((1, 3, 1,))

    # Vector operations
    yield SampleInput([c(x)], 'i->')                      # sum
    yield SampleInput([c(x), c(y)], 'i,j->ij')            # outer

    # Matrix operations
    yield SampleInput([c(A)], "ij->i")                    # col sum
    yield SampleInput([c(A), c(B)], "ij,kj->ik")          # matmul
    yield SampleInput([c(A), c(E)], "ij,Ab->ijAb")        # matrix outer product

    # Tensor operations
    yield SampleInput([c(C), c(D)], "aij,ajk->aik")       # batch matmul
    yield SampleInput([c(D), c(E)], "aij,jk->aik")        # tensor matrix contraction
    yield SampleInput([c(C), c(B)], "ijk,ik->j")          # non contiguous

    # Test diagonals
    yield SampleInput([c(I)], 'iji->j')                   # non-contiguous trace

    # Test ellipsis
    yield SampleInput([c(H)], "i...->...")
    yield SampleInput([c(C), c(x)], '...ik, ...j -> ij')

