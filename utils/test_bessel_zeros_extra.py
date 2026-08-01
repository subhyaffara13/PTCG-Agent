
def test_bessel_zeros_extra():
    mp.dps = 15
    for v in range(V):
        for m in range(1,M+1):
            print(v, m, "of", V, M)
            # Twice to test cache (if used)
            assert besseljzero(v,m).ae(jn_small_zeros[v][m-1])
            assert besseljzero(v,m).ae(jn_small_zeros[v][m-1])
            assert besseljzero(v,m,1).ae(jnp_small_zeros[v][m-1])
            assert besseljzero(v,m,1).ae(jnp_small_zeros[v][m-1])
            assert besselyzero(v,m).ae(yn_small_zeros[v][m-1])
            assert besselyzero(v,m).ae(yn_small_zeros[v][m-1])
            assert besselyzero(v,m,1).ae(ynp_small_zeros[v][m-1])
            assert besselyzero(v,m,1).ae(ynp_small_zeros[v][m-1])

