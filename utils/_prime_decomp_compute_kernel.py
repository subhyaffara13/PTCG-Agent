
def _prime_decomp_compute_kernel(I, p, ZK):
    r"""
    Parameters
    ==========

    I : :py:class:`~.Module`
        An ideal of ``ZK/pZK``.
    p : int
        The rational prime being factored.
    ZK : :py:class:`~.Submodule`
        The maximal order.

    Returns
    =======

    Pair ``(N, G)``, where:

        ``N`` is a :py:class:`~.Module` representing the kernel of the map
        ``a |--> a**p - a`` on ``(O/pO)/I``, guaranteed to be a module with
        unity.

        ``G`` is a :py:class:`~.Module` representing a basis for the separable
        algebra ``A = O/I`` (see Cohen).

    """
    W = I.matrix
    n, r = W.shape
    # Want to take the Fp-basis given by the columns of I, adjoin (1, 0, ..., 0)
    # (which we know is not already in there since I is a basis for a prime ideal)
    # and then supplement this with additional columns to make an invertible n x n
    # matrix. This will then represent a full basis for ZK, whose first r columns
    # are pullbacks of the basis for I.
    if r == 0:
        B = W.eye(n, ZZ)
    else:
        B = W.hstack(W.eye(n, ZZ)[:, 0])
    if B.shape[1] < n:
        B = supplement_a_subspace(B.convert_to(FF(p))).convert_to(ZZ)

    G = ZK.submodule_from_matrix(B)
    # Must compute G's multiplication table _before_ discarding the first r
    # columns. (See Step 9 in Alg 6.2.9 in Cohen, where the betas are actually
    # needed in order to represent each product of gammas. However, once we've
    # found the representations, then we can ignore the betas.)
    G.compute_mult_tab()
    G = G.discard_before(r)

    phi = ModuleEndomorphism(G, lambda x: x**p - x)
    N = phi.kernel(modulus=p)
    assert N.starts_with_unity()
    return N, G

