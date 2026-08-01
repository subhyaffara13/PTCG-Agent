
def test_newtons_method_function__rtol_cse_nan():
    a, b, c, N_geo, N_tot = symbols('a b c N_geo N_tot', real=True, nonnegative=True)
    i = Symbol('i', integer=True, nonnegative=True)
    N_ari = N_tot - N_geo - 1
    delta_ari = (c-b)/N_ari
    ln_delta_geo = log(b) + log(-expm1((log(a)-log(b))/N_geo))
    eqb_log = ln_delta_geo - log(delta_ari)

    def _clamp(low, expr, high):
        return Min(Max(low, expr), high)

    meth_kw = {
        'clamped_newton': {'delta_fn': lambda e, x: _clamp(
            (sqrt(a*x)-x)*0.99,
            -e/e.diff(x),
            (sqrt(c*x)-x)*0.99
        )},
        'halley': {'delta_fn': lambda e, x: (-2*(e*e.diff(x))/(2*e.diff(x)**2 - e*e.diff(x, 2)))},
        'halley_alt': {'delta_fn': lambda e, x: (-e/e.diff(x)/(1-e/e.diff(x)*e.diff(x,2)/2/e.diff(x)))},
    }
    args = eqb_log, b
    for use_cse in [False, True]:
        kwargs = {
            'params': (b, a, c, N_geo, N_tot), 'itermax': 60, 'debug': True, 'cse': use_cse,
            'counter': i, 'atol': 1e-100, 'rtol': 2e-16, 'bounds': (a,c),
            'handle_nan': Raise(RuntimeError_(QuotedString("encountered NaN.")))
        }
        func = {k: newtons_method_function(*args, func_name=f"{k}_b", **dict(kwargs, **kw)) for k, kw in meth_kw.items()}
        py_mod = {k: py_module(v) for k, v in func.items()}
        namespace = {}
        root_find_b = {}
        for k, v in py_mod.items():
            ns = namespace[k] = {}
            exec(v, ns, ns)
            root_find_b[k] = ns[f'{k}_b']
        ref = Float('13.2261515064168768938151923226496')
        reftol = {'clamped_newton': 2e-16, 'halley': 2e-16, 'halley_alt': 3e-16}
        guess = 4.0
        for meth, func in root_find_b.items():
            result = func(guess, 1e-2, 1e2, 50, 100)
            req = ref*reftol[meth]
            if use_cse:
                req *= 2
            assert abs(result - ref) < req

