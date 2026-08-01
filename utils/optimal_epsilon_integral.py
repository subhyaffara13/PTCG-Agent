
def optimal_epsilon_integral():
    """Fit optimal choice of epsilon for integral representation.

    The integrand of
        int_0^pi P(eps, a, b, x, phi) * dphi
    can exhibit oscillatory behaviour. It stems from the cosine of P and can be
    minimized by minimizing the arc length of the argument
        f(phi) = eps * sin(phi) - x * eps^(-a) * sin(a * phi) + (1 - b) * phi
    of cos(f(phi)).
    We minimize the arc length in eps for a grid of values (a, b, x) and fit a
    parametric function to it.
    """
    def fp(eps, a, b, x, phi):
        """Derivative of f w.r.t. phi."""
        eps_a = np.power(1. * eps, -a)
        return eps * np.cos(phi) - a * x * eps_a * np.cos(a * phi) + 1 - b

    def arclength(eps, a, b, x, epsrel=1e-2, limit=100):
        """Compute Arc length of f.

        Note that the arc length of a function f from t0 to t1 is given by
            int_t0^t1 sqrt(1 + f'(t)^2) dt
        """
        return quad(lambda phi: np.sqrt(1 + fp(eps, a, b, x, phi)**2),
                    0, np.pi,
                    epsrel=epsrel, limit=100)[0]

    # grid of minimal arc length values
    data_a = [1e-3, 0.1, 0.5, 0.9, 1, 2, 4, 5, 6, 8]
    data_b = [0, 1, 4, 7, 10]
    data_x = [1, 1.5, 2, 4, 10, 20, 50, 100, 200, 500, 1e3, 5e3, 1e4]
    data_a, data_b, data_x = np.meshgrid(data_a, data_b, data_x)
    data_a, data_b, data_x = (data_a.flatten(), data_b.flatten(),
                              data_x.flatten())
    best_eps = []
    for i in range(data_x.size):
        best_eps.append(
            minimize_scalar(lambda eps: arclength(eps, data_a[i], data_b[i],
                                                  data_x[i]),
                            bounds=(1e-3, 1000),
                            method='Bounded', options={'xatol': 1e-3}).x
        )
    best_eps = np.array(best_eps)
    # pandas would be nice, but here a dictionary is enough
    df = {'a': data_a,
          'b': data_b,
          'x': data_x,
          'eps': best_eps,
          }

    def func(data, A0, A1, A2, A3, A4, A5):
        """Compute parametric function to fit."""
        a = data['a']
        b = data['b']
        x = data['x']
        return (A0 * b * np.exp(-0.5 * a)
                + np.exp(A1 + 1 / (1 + a) * np.log(x) - A2 * np.exp(-A3 * a)
                         + A4 / (1 + np.exp(A5 * a))))

    func_params = list(curve_fit(func, df, df['eps'], method='trf')[0])

    s = "Fit optimal eps for integrand P via minimal arc length\n"
    s += "with parametric function:\n"
    s += "optimal_eps = (A0 * b * exp(-a/2) + exp(A1 + 1 / (1 + a) * log(x)\n"
    s += "              - A2 * exp(-A3 * a) + A4 / (1 + exp(A5 * a)))\n\n"
    s += "Fitted parameters A0 to A5 are:\n"
    s += ', '.join([f'{x:.5g}' for x in func_params])
    return s

