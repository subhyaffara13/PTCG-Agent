
def test_newtons_method_function__pycode():
    x = Symbol('x', real=True)
    expr = cos(x) - x**3
    func = newtons_method_function(expr, x)
    py_mod = py_module(func)
    namespace = {}
    exec(py_mod, namespace, namespace)
    res = eval('newton(0.5)', namespace)
    assert abs(res - 0.865474033102) < 1e-12

