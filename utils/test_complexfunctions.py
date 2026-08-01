
def test_complexfunctions():
    dtypes = {x:'complex128', y:'complex128'}
    with warns_deprecated_sympy():
        xt, yt = aesara_code(x, dtypes=dtypes), aesara_code(y, dtypes=dtypes)
    from sympy.functions.elementary.complexes import conjugate
    from aesara.tensor import as_tensor_variable as atv
    from aesara.tensor import complex as cplx
    with warns_deprecated_sympy():
        assert theq(aesara_code(y*conjugate(x), dtypes=dtypes), yt*(xt.conj()))
        assert theq(aesara_code((1+2j)*x), xt*(atv(1.0)+atv(2.0)*cplx(0,1)))


def test_complexfunctions():
    with warns_deprecated_sympy():
        xt, yt = theano_code_(x, dtypes={x:'complex128'}), theano_code_(y, dtypes={y: 'complex128'})
    from sympy.functions.elementary.complexes import conjugate
    from theano.tensor import as_tensor_variable as atv
    from theano.tensor import complex as cplx
    with warns_deprecated_sympy():
        assert theq(theano_code_(y*conjugate(x)), yt*(xt.conj()))
        assert theq(theano_code_((1+2j)*x), xt*(atv(1.0)+atv(2.0)*cplx(0,1)))

