
def nichols_plot_expr(system):
    """Function to get the expression for Nichols plot."""
    s = system.var
    w = Dummy('w', real=True)
    sys_expr = system.to_expr()
    H_jw = sys_expr.subs(s, I*w)
    mag_expr = Abs(H_jw)
    mag_dB_expr = 20*log(mag_expr, 10)
    phase_expr = arg(H_jw)
    phase_deg_expr = deg(phase_expr)
    return mag_dB_expr, phase_deg_expr, w

