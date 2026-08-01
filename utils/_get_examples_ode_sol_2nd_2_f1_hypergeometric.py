
def _get_examples_ode_sol_2nd_2F1_hypergeometric():
    return {
            'hint': "2nd_hypergeometric",
            'func': f(x),
            'examples':{
    '2nd_2F1_hyper_01': {
        'eq': x*(x-1)*f(x).diff(x, 2) + (S(3)/2 -2*x)*f(x).diff(x) + 2*f(x),
        'sol': [Eq(f(x), C1*x**(S(5)/2)*hyper((S(3)/2, S(1)/2), (S(7)/2,), x) + C2*hyper((-1, -2), (-S(3)/2,), x))],
    },

    '2nd_2F1_hyper_02': {
        'eq': x*(x-1)*f(x).diff(x, 2) + (S(7)/2*x)*f(x).diff(x) + f(x),
        'sol': [Eq(f(x), (C1*(1 - x)**(S(5)/2)*hyper((S(1)/2, 2), (S(7)/2,), 1 - x) +
          C2*hyper((-S(1)/2, -2), (-S(3)/2,), 1 - x))/(x - 1)**(S(5)/2))],
    },

    '2nd_2F1_hyper_03': {
        'eq': x*(x-1)*f(x).diff(x, 2) + (S(3)+ S(7)/2*x)*f(x).diff(x) + f(x),
        'sol': [Eq(f(x), (C1*(1 - x)**(S(11)/2)*hyper((S(1)/2, 2), (S(13)/2,), 1 - x) +
          C2*hyper((-S(7)/2, -5), (-S(9)/2,), 1 - x))/(x - 1)**(S(11)/2))],
    },

    '2nd_2F1_hyper_04': {
        'eq': -x**(S(5)/7)*(-416*x**(S(9)/7)/9 - 2385*x**(S(5)/7)/49 + S(298)*x/3)*f(x)/(196*(-x**(S(6)/7) +
         x)**2*(x**(S(6)/7) + x)**2) + Derivative(f(x), (x, 2)),
        'sol': [Eq(f(x), x**(S(45)/98)*(C1*x**(S(4)/49)*hyper((S(1)/3, -S(1)/2), (S(9)/7,), x**(S(2)/7)) +
          C2*hyper((S(1)/21, -S(11)/14), (S(5)/7,), x**(S(2)/7)))/(x**(S(2)/7) - 1)**(S(19)/84))],
        'checkodesol_XFAIL':True,
    },
    }
    }

