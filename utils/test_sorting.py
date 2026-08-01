
def test_sorting():
    i, j = symbols('i,j', below_fermi=True)
    a, b = symbols('a,b', above_fermi=True)
    p, q = symbols('p,q')

    # p, q
    assert _sort_anticommuting_fermions([Fd(p), F(q)]) == ([Fd(p), F(q)], 0)
    assert _sort_anticommuting_fermions([F(p), Fd(q)]) == ([Fd(q), F(p)], 1)

    # i, p
    assert _sort_anticommuting_fermions([F(p), Fd(i)]) == ([F(p), Fd(i)], 0)
    assert _sort_anticommuting_fermions([Fd(i), F(p)]) == ([F(p), Fd(i)], 1)
    assert _sort_anticommuting_fermions([Fd(p), Fd(i)]) == ([Fd(p), Fd(i)], 0)
    assert _sort_anticommuting_fermions([Fd(i), Fd(p)]) == ([Fd(p), Fd(i)], 1)
    assert _sort_anticommuting_fermions([F(p), F(i)]) == ([F(i), F(p)], 1)
    assert _sort_anticommuting_fermions([F(i), F(p)]) == ([F(i), F(p)], 0)
    assert _sort_anticommuting_fermions([Fd(p), F(i)]) == ([F(i), Fd(p)], 1)
    assert _sort_anticommuting_fermions([F(i), Fd(p)]) == ([F(i), Fd(p)], 0)

    # a, p
    assert _sort_anticommuting_fermions([F(p), Fd(a)]) == ([Fd(a), F(p)], 1)
    assert _sort_anticommuting_fermions([Fd(a), F(p)]) == ([Fd(a), F(p)], 0)
    assert _sort_anticommuting_fermions([Fd(p), Fd(a)]) == ([Fd(a), Fd(p)], 1)
    assert _sort_anticommuting_fermions([Fd(a), Fd(p)]) == ([Fd(a), Fd(p)], 0)
    assert _sort_anticommuting_fermions([F(p), F(a)]) == ([F(p), F(a)], 0)
    assert _sort_anticommuting_fermions([F(a), F(p)]) == ([F(p), F(a)], 1)
    assert _sort_anticommuting_fermions([Fd(p), F(a)]) == ([Fd(p), F(a)], 0)
    assert _sort_anticommuting_fermions([F(a), Fd(p)]) == ([Fd(p), F(a)], 1)

    # i, a
    assert _sort_anticommuting_fermions([F(i), Fd(j)]) == ([F(i), Fd(j)], 0)
    assert _sort_anticommuting_fermions([Fd(j), F(i)]) == ([F(i), Fd(j)], 1)
    assert _sort_anticommuting_fermions([Fd(a), Fd(i)]) == ([Fd(a), Fd(i)], 0)
    assert _sort_anticommuting_fermions([Fd(i), Fd(a)]) == ([Fd(a), Fd(i)], 1)
    assert _sort_anticommuting_fermions([F(a), F(i)]) == ([F(i), F(a)], 1)
    assert _sort_anticommuting_fermions([F(i), F(a)]) == ([F(i), F(a)], 0)

