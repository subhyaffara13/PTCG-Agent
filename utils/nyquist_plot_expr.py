
def nyquist_plot_expr(system):
    """Function to get the expression for Nyquist plot."""
    s = system.var
    w = Dummy('w', real=True)
    repl = I * w
    expr = system.to_expr()
    w_expr = expr.subs({s: repl})
    w_expr = w_expr.as_real_imag()
    real_expr = w_expr[0]
    imag_expr = w_expr[1]
    return real_expr, imag_expr, w

