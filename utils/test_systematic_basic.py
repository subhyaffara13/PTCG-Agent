
def test_systematic_basic():
    def s(sympy_object, numpy_array):
        _ = [sympy_object + numpy_array,
        numpy_array + sympy_object,
        sympy_object - numpy_array,
        numpy_array - sympy_object,
        sympy_object * numpy_array,
        numpy_array * sympy_object,
        sympy_object / numpy_array,
        numpy_array / sympy_object,
        sympy_object ** numpy_array,
        numpy_array ** sympy_object]
    x = Symbol("x")
    y = Symbol("y")
    sympy_objs = [
        Rational(2, 3),
        Float("1.3"),
        x,
        y,
        pow(x, y)*y,
        Integer(5),
        Float(5.5),
    ]
    numpy_objs = [
        array([1]),
        array([3, 8, -1]),
        array([x, x**2, Rational(5)]),
        array([x/y*sin(y), 5, Rational(5)]),
    ]
    for x in sympy_objs:
        for y in numpy_objs:
            s(x, y)

