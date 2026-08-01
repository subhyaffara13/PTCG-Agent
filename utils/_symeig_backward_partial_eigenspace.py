
def _symeig_backward_partial_eigenspace(D_grad, U_grad, A, D, U, largest):
    # compute a projection operator onto an orthogonal subspace spanned by the
    # columns of U defined as (I - UU^T)
    Ut = U.mT.contiguous()
    proj_U_ortho = -U.matmul(Ut)
    proj_U_ortho.diagonal(dim1=-2, dim2=-1).add_(1)

    # compute U_ortho, a basis for the orthogonal complement to the span(U),
    # by projecting a random [..., m, m - k] matrix onto the subspace spanned
    # by the columns of U.
    #
    # fix generator for determinism
    gen = torch.Generator(A.device)

    # orthogonal complement to the span(U)
    U_ortho = proj_U_ortho.matmul(
        torch.randn(
            (*A.shape[:-1], A.size(-1) - D.size(-1)),
            dtype=A.dtype,
            device=A.device,
            generator=gen,
        )
    )
    U_ortho_t = U_ortho.mT.contiguous()

    # compute the coefficients of the characteristic polynomial of the tensor D.
    # Note that D is diagonal, so the diagonal elements are exactly the roots
    # of the characteristic polynomial.
    chr_poly_D = _polynomial_coefficients_given_roots(D)

    # the code below finds the explicit solution to the Sylvester equation
    # U_ortho^T A U_ortho dX - dX D = -U_ortho^T A U
    # and incorporates it into the whole gradient stored in the `res` variable.
    #
    # Equivalent to the following naive implementation:
    # res = A.new_zeros(A.shape)
    # p_res = A.new_zeros(*A.shape[:-1], D.size(-1))
    # for k in range(1, chr_poly_D.size(-1)):
    #     p_res.zero_()
    #     for i in range(0, k):
    #         p_res += (A.matrix_power(k - 1 - i) @ U_grad) * D.pow(i).unsqueeze(-2)
    #     res -= chr_poly_D[k] * (U_ortho @ poly_D_at_A.inverse() @ U_ortho_t @  p_res @ U.t())
    #
    # Note that dX is a differential, so the gradient contribution comes from the backward sensitivity
    # Tr(f(U_grad, D_grad, A, U, D)^T dX) = Tr(g(U_grad, A, U, D)^T dA) for some functions f and g,
    # and we need to compute g(U_grad, A, U, D)
    #
    # The naive implementation is based on the paper
    # Hu, Qingxi, and Daizhan Cheng.
    # "The polynomial solution to the Sylvester matrix equation."
    # Applied mathematics letters 19.9 (2006): 859-864.
    #
    # We can modify the computation of `p_res` from above in a more efficient way
    # p_res =   U_grad * (chr_poly_D[1] * D.pow(0) + ... + chr_poly_D[k] * D.pow(k)).unsqueeze(-2)
    #       + A U_grad * (chr_poly_D[2] * D.pow(0) + ... + chr_poly_D[k] * D.pow(k - 1)).unsqueeze(-2)
    #       + ...
    #       + A.matrix_power(k - 1) U_grad * chr_poly_D[k]
    # Note that this saves us from redundant matrix products with A (elimination of matrix_power)
    U_grad_projected = U_grad
    series_acc = U_grad_projected.new_zeros(U_grad_projected.shape)
    for k in range(1, chr_poly_D.size(-1)):
        poly_D = _vector_polynomial_value(chr_poly_D[..., k:], D)
        series_acc += U_grad_projected * poly_D.unsqueeze(-2)
        U_grad_projected = A.matmul(U_grad_projected)

    # compute chr_poly_D(A) which essentially is:
    #
    # chr_poly_D_at_A = A.new_zeros(A.shape)
    # for k in range(chr_poly_D.size(-1)):
    #     chr_poly_D_at_A += chr_poly_D[k] * A.matrix_power(k)
    #
    # Note, however, for better performance we use the Horner's rule
    chr_poly_D_at_A = _matrix_polynomial_value(chr_poly_D, A)

    # compute the action of `chr_poly_D_at_A` restricted to U_ortho_t
    chr_poly_D_at_A_to_U_ortho = torch.matmul(
        U_ortho_t, torch.matmul(chr_poly_D_at_A, U_ortho)
    )
    # we need to invert 'chr_poly_D_at_A_to_U_ortho`, for that we compute its
    # Cholesky decomposition and then use `torch.cholesky_solve` for better stability.
    # Cholesky decomposition requires the input to be positive-definite.
    # Note that `chr_poly_D_at_A_to_U_ortho` is positive-definite if
    # 1. `largest` == False, or
    # 2. `largest` == True and `k` is even
    # under the assumption that `A` has distinct eigenvalues.
    #
    # check if `chr_poly_D_at_A_to_U_ortho` is positive-definite or negative-definite
    chr_poly_D_at_A_to_U_ortho_sign = -1 if (largest and (k % 2 == 1)) else +1
    chr_poly_D_at_A_to_U_ortho_L = torch.linalg.cholesky(
        chr_poly_D_at_A_to_U_ortho_sign * chr_poly_D_at_A_to_U_ortho
    )

    # compute the gradient part in span(U)
    res = _symeig_backward_complete_eigenspace(D_grad, U_grad, A, D, U)

    # incorporate the Sylvester equation solution into the full gradient
    # it resides in span(U_ortho)
    res -= U_ortho.matmul(
        chr_poly_D_at_A_to_U_ortho_sign
        * torch.cholesky_solve(
            U_ortho_t.matmul(series_acc), chr_poly_D_at_A_to_U_ortho_L
        )
    ).matmul(Ut)

    return res

