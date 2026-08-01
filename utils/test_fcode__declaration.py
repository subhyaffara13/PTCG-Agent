
def test_fcode_Declaration():
    def check(expr, ref, **kwargs):
        assert fcode(expr, standard=95, source_format='free', **kwargs) == ref

    i = symbols('i', integer=True)
    var1 = Variable.deduced(i)
    dcl1 = Declaration(var1)
    check(dcl1, "integer*4 :: i")


    x, y = symbols('x y')
    var2 = Variable(x, float32, value=42, attrs={value_const})
    dcl2b = Declaration(var2)
    check(dcl2b, 'real*4, parameter :: x = 42')

    var3 = Variable(y, type=bool_)
    dcl3 = Declaration(var3)
    check(dcl3, 'logical :: y')

    check(float32, "real*4")
    check(float64, "real*8")
    check(real, "real*4", type_aliases={real: float32})
    check(real, "real*8", type_aliases={real: float64})

