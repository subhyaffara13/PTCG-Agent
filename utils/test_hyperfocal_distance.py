
def test_hyperfocal_distance():
    f, N, c = symbols('f, N, c')
    assert hyperfocal_distance(f=f, N=N, c=c) == f**2/(N*c)
    assert ae(hyperfocal_distance(f=0.5, N=8, c=0.0033), 9.47, 2)

