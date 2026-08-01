
def nyquist_plot(system, initial_omega=0.01, final_omega=100, show=True,
                color='b', **kwargs):
    r"""
    Generates the Nyquist plot for a continuous-time system.

    Parameters
    ==========

    system : SISOLinearTimeInvariant
        The LTI SISO system for which the Nyquist plot is to be generated.
    initial_omega : float, optional
        The starting frequency value. Defaults to 0.01.
    final_omega : float, optional
        The ending frequency value. Defaults to 100.
    show : bool, optional
        If True, the plot is displayed. Default is True.
    color : str, optional
        The color of the Nyquist plot. Default is 'b' (blue).
    grid : bool, optional
        If True, grid lines are displayed. Default is False.
    **kwargs
        Additional keyword arguments for customization.

    Examples
    ========

    .. plot::
        :context: close-figs
        :format: doctest
        :include-source: True

        >>> from sympy.abc import s
        >>> from sympy.physics.control.lti import TransferFunction
        >>> from sympy.physics.control.control_plots import nyquist_plot
        >>> tf1 = TransferFunction(2*s**2 + 5*s + 1, s**2 + 2*s + 3, s)
        >>> nyquist_plot(tf1)   # doctest: +SKIP

    See Also
    ========

    nichols_plot, bode_plot

    """
    _check_system(system)
    real_expr, imag_expr, w = nyquist_plot_expr(system)
    w_values = [(w, initial_omega, final_omega)]
    p = plot_parametric(
        (real_expr, imag_expr),   # The curve
        (real_expr, -imag_expr),  # Its mirror image
        *w_values,
        show=False,
        line_color=color,
        adaptive=True,
        title=f'Nyquist Plot of ${latex(system)}$',
        xlabel='Real Axis',
        ylabel='Imaginary Axis',
        size=(6, 5),
        kwargs=kwargs)
    if show:
        p.show()
        return
    return p

