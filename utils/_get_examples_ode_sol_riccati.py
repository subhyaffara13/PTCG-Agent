
def _get_examples_ode_sol_riccati():
    # Type: Riccati special alpha = -2, a*dy/dx + b*y**2 + c*y/x +d/x**2
    return {
            'hint': "Riccati_special_minus2",
            'func': f(x),
            'examples':{
    'riccati_01': {
        'eq': 2*f(x).diff(x) + f(x)**2 - f(x)/x + 3*x**(-2),
        'sol': [Eq(f(x), (-sqrt(3)*tan(C1 + sqrt(3)*log(x)/4) + 3)/(2*x))],
    },
    },
    }

