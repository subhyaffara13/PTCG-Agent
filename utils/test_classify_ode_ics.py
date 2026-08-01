
def test_classify_ode_ics():
    # Dummy
    eq = f(x).diff(x, x) - f(x)

    # Not f(0) or f'(0)
    ics = {x: 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))


    ############################
    # f(0) type (AppliedUndef) #
    ############################


    # Wrong function
    ics = {g(0): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Contains x
    ics = {f(x): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Too many args
    ics = {f(0, 0): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # point contains x
    ics = {f(0): f(x)}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Does not raise
    ics = {f(0): f(0)}
    classify_ode(eq, f(x), ics=ics)

    # Does not raise
    ics = {f(0): 1}
    classify_ode(eq, f(x), ics=ics)


    #####################
    # f'(0) type (Subs) #
    #####################

    # Wrong function
    ics = {g(x).diff(x).subs(x, 0): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Contains x
    ics = {f(y).diff(y).subs(y, x): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Wrong variable
    ics = {f(y).diff(y).subs(y, 0): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Too many args
    ics = {f(x, y).diff(x).subs(x, 0): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Derivative wrt wrong vars
    ics = {Derivative(f(x), x, y).subs(x, 0): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # point contains x
    ics = {f(x).diff(x).subs(x, 0): f(x)}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Does not raise
    ics = {f(x).diff(x).subs(x, 0): f(x).diff(x).subs(x, 0)}
    classify_ode(eq, f(x), ics=ics)

    # Does not raise
    ics = {f(x).diff(x).subs(x, 0): 1}
    classify_ode(eq, f(x), ics=ics)

    ###########################
    # f'(y) type (Derivative) #
    ###########################

    # Wrong function
    ics = {g(x).diff(x).subs(x, y): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Contains x
    ics = {f(y).diff(y).subs(y, x): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Too many args
    ics = {f(x, y).diff(x).subs(x, y): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Derivative wrt wrong vars
    ics = {Derivative(f(x), x, z).subs(x, y): 1}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # point contains x
    ics = {f(x).diff(x).subs(x, y): f(x)}
    raises(ValueError, lambda: classify_ode(eq, f(x), ics=ics))

    # Does not raise
    ics = {f(x).diff(x).subs(x, 0): f(0)}
    classify_ode(eq, f(x), ics=ics)

    # Does not raise
    ics = {f(x).diff(x).subs(x, y): 1}
    classify_ode(eq, f(x), ics=ics)

