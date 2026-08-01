
def test_integral_transforms():
    x = Symbol("x")
    k = Symbol("k")
    f = Function("f")
    a = Symbol("a")
    b = Symbol("b")

    assert latex(MellinTransform(f(x), x, k)) == \
        r"\mathcal{M}_{x}\left[f{\left(x \right)}\right]\left(k\right)"
    assert latex(InverseMellinTransform(f(k), k, x, a, b)) == \
        r"\mathcal{M}^{-1}_{k}\left[f{\left(k \right)}\right]\left(x\right)"

    assert latex(LaplaceTransform(f(x), x, k)) == \
        r"\mathcal{L}_{x}\left[f{\left(x \right)}\right]\left(k\right)"
    assert latex(InverseLaplaceTransform(f(k), k, x, (a, b))) == \
        r"\mathcal{L}^{-1}_{k}\left[f{\left(k \right)}\right]\left(x\right)"

    assert latex(FourierTransform(f(x), x, k)) == \
        r"\mathcal{F}_{x}\left[f{\left(x \right)}\right]\left(k\right)"
    assert latex(InverseFourierTransform(f(k), k, x)) == \
        r"\mathcal{F}^{-1}_{k}\left[f{\left(k \right)}\right]\left(x\right)"

    assert latex(CosineTransform(f(x), x, k)) == \
        r"\mathcal{COS}_{x}\left[f{\left(x \right)}\right]\left(k\right)"
    assert latex(InverseCosineTransform(f(k), k, x)) == \
        r"\mathcal{COS}^{-1}_{k}\left[f{\left(k \right)}\right]\left(x\right)"

    assert latex(SineTransform(f(x), x, k)) == \
        r"\mathcal{SIN}_{x}\left[f{\left(x \right)}\right]\left(k\right)"
    assert latex(InverseSineTransform(f(k), k, x)) == \
        r"\mathcal{SIN}^{-1}_{k}\left[f{\left(k \right)}\right]\left(x\right)"

