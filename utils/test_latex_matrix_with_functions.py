
def test_latex_matrix_with_functions():
    t = symbols('t')
    theta1 = symbols('theta1', cls=Function)

    M = Matrix([[sin(theta1(t)), cos(theta1(t))],
                [cos(theta1(t).diff(t)), sin(theta1(t).diff(t))]])

    expected = (r'\left[\begin{matrix}\sin{\left('
                r'\theta_{1}{\left(t \right)} \right)} & '
                r'\cos{\left(\theta_{1}{\left(t \right)} \right)'
                r'}\\\cos{\left(\frac{d}{d t} \theta_{1}{\left(t '
                r'\right)} \right)} & \sin{\left(\frac{d}{d t} '
                r'\theta_{1}{\left(t \right)} \right'
                r')}\end{matrix}\right]')

    assert latex(M) == expected

