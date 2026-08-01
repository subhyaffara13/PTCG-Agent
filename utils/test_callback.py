
def test_callback():
    e = a + 1.2
    f = g.llvm_callable([a], e, callback_type='scipy.integrate.test')
    m = ctypes.c_int(1)
    array_type = ctypes.c_double * 1
    inp = {a: 2.2}
    array = array_type(inp[a])
    jit_res = f(m, array)

    res = float(e.subs(inp).evalf())

    assert isclose(jit_res, res)


def test_callback():
    # test that callback function works as expected

    results = []
    
    def my_callback_optimresult(intermediate_result: OptimizeResult):
        results.append(intermediate_result)
        
    def my_callback_x(x):
        r = OptimizeResult()
        r.nit = 1
        r.x = x
        results.append(r)
        return False
        
    def my_callback_optimresult_stop_exception(
        intermediate_result: OptimizeResult):
        results.append(intermediate_result)
        raise StopIteration

    def my_callback_x_stop_exception(x):
        r = OptimizeResult()
        r.nit = 1
        r.x = x
        results.append(r)
        raise StopIteration

    # Try for different function signatures and stop methods
    callbacks_nostop = [my_callback_optimresult, my_callback_x]
    callbacks_stop = [my_callback_optimresult_stop_exception,
                      my_callback_x_stop_exception]
    
    # Try for all the implemented methods: trf, trf_bounds and dogbox
    calls = [
        lambda callback: least_squares(fun_trivial, 5.0, method='trf', 
                                       callback=callback),
        lambda callback: least_squares(fun_trivial, 5.0, method='trf', 
                                       bounds=(-8.0, 8.0), callback=callback),
        lambda callback: least_squares(fun_trivial, 5.0, method='dogbox', 
                                       callback=callback)
    ]

    for mycallback, call in product(callbacks_nostop, calls):
        results.clear()
        # Call the different implemented methods
        res = call(mycallback)
        # Check that callback was called
        assert len(results) > 0
        # Check that results data makes sense
        assert results[-1].nit > 0
        # Check that it didn't stop because of the callback
        assert res.status != -2
        # final callback x should be same as final result
        assert_allclose(results[-1].x, res.x)

    for mycallback, call in product(callbacks_stop, calls):
        results.clear()
        # Call the different implemented methods
        res = call(mycallback)
        # Check that callback was called
        assert len(results) > 0
        # Check that only one iteration was run
        assert results[-1].nit == 1
        # Check that it stopped because of the callback
        assert res.status == -2

