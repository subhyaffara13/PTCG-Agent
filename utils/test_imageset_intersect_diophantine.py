
def test_imageset_intersect_diophantine():
    from sympy.abc import m, n
    # Check that same lambda variable for both ImageSets is handled correctly
    img1 = ImageSet(Lambda(n, 2*n + 1), S.Integers)
    img2 = ImageSet(Lambda(n, 4*n + 1), S.Integers)
    assert img1.intersect(img2) == img2
    # Empty solution set returned by diophantine:
    assert ImageSet(Lambda(n, 2*n), S.Integers).intersect(
            ImageSet(Lambda(n, 2*n + 1), S.Integers)) == S.EmptySet
    # Check intersection with S.Integers:
    assert ImageSet(Lambda(n, 9/n + 20*n/3), S.Integers).intersect(
            S.Integers) == FiniteSet(-61, -23, 23, 61)
    # Single solution (2, 3) for diophantine solution:
    assert ImageSet(Lambda(n, (n - 2)**2), S.Integers).intersect(
            ImageSet(Lambda(n, -(n - 3)**2), S.Integers)) == FiniteSet(0)
    # Single parametric solution for diophantine solution:
    assert ImageSet(Lambda(n, n**2 + 5), S.Integers).intersect(
            ImageSet(Lambda(m, 2*m), S.Integers)).dummy_eq(ImageSet(
            Lambda(n, 4*n**2 + 4*n + 6), S.Integers))
    # 4 non-parametric solution couples for dioph. equation:
    assert ImageSet(Lambda(n, n**2 - 9), S.Integers).intersect(
            ImageSet(Lambda(m, -m**2), S.Integers)) == FiniteSet(-9, 0)
    # Double parametric solution for diophantine solution:
    assert ImageSet(Lambda(m, m**2 + 40), S.Integers).intersect(
            ImageSet(Lambda(n, 41*n), S.Integers)).dummy_eq(Intersection(
            ImageSet(Lambda(m, m**2 + 40), S.Integers),
            ImageSet(Lambda(n, 41*n), S.Integers)))
    # Check that diophantine returns *all* (8) solutions (permute=True)
    assert ImageSet(Lambda(n, n**4 - 2**4), S.Integers).intersect(
            ImageSet(Lambda(m, -m**4 + 3**4), S.Integers)) == FiniteSet(0, 65)
    assert ImageSet(Lambda(n, pi/12 + n*5*pi/12), S.Integers).intersect(
            ImageSet(Lambda(n, 7*pi/12 + n*11*pi/12), S.Integers)).dummy_eq(ImageSet(
            Lambda(n, 55*pi*n/12 + 17*pi/4), S.Integers))
    # TypeError raised by diophantine (#18081)
    assert ImageSet(Lambda(n, n*log(2)), S.Integers).intersection(
        S.Integers).dummy_eq(Intersection(ImageSet(
        Lambda(n, n*log(2)), S.Integers), S.Integers))
    # NotImplementedError raised by diophantine (no solver for cubic_thue)
    assert ImageSet(Lambda(n, n**3 + 1), S.Integers).intersect(
            ImageSet(Lambda(n, n**3), S.Integers)).dummy_eq(Intersection(
            ImageSet(Lambda(n, n**3 + 1), S.Integers),
            ImageSet(Lambda(n, n**3), S.Integers)))

