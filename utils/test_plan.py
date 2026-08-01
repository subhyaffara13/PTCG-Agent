
def test_plan():
    assert devise_plan(Hyper_Function([0], ()),
            Hyper_Function([0], ()), z) == []
    with raises(ValueError):
        devise_plan(Hyper_Function([1], ()), Hyper_Function((), ()), z)
    with raises(ValueError):
        devise_plan(Hyper_Function([2], [1]), Hyper_Function([2], [2]), z)
    with raises(ValueError):
        devise_plan(Hyper_Function([2], []), Hyper_Function([S("1/2")], []), z)

    # We cannot use pi/(10000 + n) because polys is insanely slow.
    a1, a2, b1 = (randcplx(n) for n in range(3))
    b1 += 2*I
    h = hyper([a1, a2], [b1], z)

    h2 = hyper((a1 + 1, a2), [b1], z)
    assert tn(apply_operators(h,
        devise_plan(Hyper_Function((a1 + 1, a2), [b1]),
            Hyper_Function((a1, a2), [b1]), z), op),
        h2, z)

    h2 = hyper((a1 + 1, a2 - 1), [b1], z)
    assert tn(apply_operators(h,
        devise_plan(Hyper_Function((a1 + 1, a2 - 1), [b1]),
            Hyper_Function((a1, a2), [b1]), z), op),
        h2, z)

