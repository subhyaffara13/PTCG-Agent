
def test_sos_consistency():
    # Consistency checks of output='sos' for the specialized IIR filter
    # design functions.
    design_funcs = [(bessel, (0.1,)),
                    (butter, (0.1,)),
                    (cheby1, (45.0, 0.1)),
                    (cheby2, (0.087, 0.1)),
                    (ellip, (0.087, 45, 0.1))]
    for func, args in design_funcs:
        name = func.__name__

        b, a = func(2, *args, output='ba')
        sos = func(2, *args, output='sos')
        xp_assert_close(sos, [np.hstack((b, a))], err_msg=f"{name}(2,...)")

        zpk = func(3, *args, output='zpk')
        sos = func(3, *args, output='sos')
        xp_assert_close(sos, zpk2sos(*zpk), err_msg=f"{name}(3,...)")

        zpk = func(4, *args, output='zpk')
        sos = func(4, *args, output='sos')
        xp_assert_close(sos, zpk2sos(*zpk), err_msg=f"{name}(4,...)")

