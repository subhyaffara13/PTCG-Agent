
def test_omega():
    Gl = nx.connected_watts_strogatz_graph(50, 6, 0, seed=rng)
    Gr = nx.connected_watts_strogatz_graph(50, 6, 1, seed=rng)
    Gs = nx.connected_watts_strogatz_graph(50, 6, 0.1, seed=rng)
    omegal = omega(Gl, niter=1, nrand=1, seed=rng)
    omegar = omega(Gr, niter=1, nrand=1, seed=rng)
    omegas = omega(Gs, niter=1, nrand=1, seed=rng)
    assert omegal < omegas and omegas < omegar

    # Test that omega lies within the [-1, 1] bounds
    G_barbell = nx.barbell_graph(5, 1)
    G_karate = nx.karate_club_graph()

    omega_barbell = nx.omega(G_barbell)
    omega_karate = nx.omega(G_karate, nrand=2)

    omegas = (omegal, omegar, omegas, omega_barbell, omega_karate)

    for o in omegas:
        assert -1 <= o <= 1

