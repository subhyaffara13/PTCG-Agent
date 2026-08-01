
def _perform_test_replacer(info, lambdify):

    x1_ = WildDot("x1_")
    x2_ = WildDot("x2_")

    a_ = WildDot("a_", optional=S.One)
    b_ = WildDot("b_", optional=S.One)
    c_ = WildDot("c_", optional=S.Zero)

    replacer = Replacer(common_constraints=[
        matchpy.CustomConstraint(lambda a_: not a_.has(x)),
        matchpy.CustomConstraint(lambda b_: not b_.has(x)),
        matchpy.CustomConstraint(lambda c_: not c_.has(x)),
    ], lambdify=lambdify, info=info)

    # Rewrite the equation into implicit form, unless it's already solved:
    replacer.add(Eq(x1_, x2_), Eq(x1_ - x2_, 0), conditions_nonfalse=[Ne(x2_, 0), Ne(x1_, 0), Ne(x1_, x), Ne(x2_, x)], info=1)

    # Simple equation solver for real numbers:
    replacer.add(Eq(a_*x + b_, 0), Eq(x, -b_/a_), info=2)
    disc = b_**2 - 4*a_*c_
    replacer.add(
        Eq(a_*x**2 + b_*x + c_, 0),
        Eq(x, (-b_ - sqrt(disc))/(2*a_)) | Eq(x, (-b_ + sqrt(disc))/(2*a_)),
        conditions_nonfalse=[disc >= 0],
        info=3
    )
    replacer.add(
        Eq(a_*x**2 + c_, 0),
        Eq(x, sqrt(-c_/a_)) | Eq(x, -sqrt(-c_/a_)),
        conditions_nonfalse=[-c_*a_ > 0],
        info=4
    )

    g = lambda expr, infos: (expr, infos) if info else expr

    assert replacer.replace(Eq(3*x, y)) == g(Eq(x, y/3), [1, 2])
    assert replacer.replace(Eq(x**2 + 1, 0)) == g(Eq(x**2 + 1, 0), [])
    assert replacer.replace(Eq(x**2, 4)) == g((Eq(x, 2) | Eq(x, -2)), [1, 4])
    assert replacer.replace(Eq(x**2 + 4*y*x + 4*y**2, 0)) == g(Eq(x, -2*y), [3])

