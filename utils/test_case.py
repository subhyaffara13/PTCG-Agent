
def test_case():
    ob = FCodePrinter()
    x,x_,x__,y,X,X_,Y = symbols('x,x_,x__,y,X,X_,Y')
    assert fcode(exp(x_) + sin(x*y) + cos(X*Y)) == \
                        '      exp(x_) + sin(x*y) + cos(X__*Y_)'
    assert fcode(exp(x__) + 2*x*Y*X_**Rational(7, 2)) == \
                        '      2*X_**(7.0d0/2.0d0)*Y*x + exp(x__)'
    assert fcode(exp(x_) + sin(x*y) + cos(X*Y), name_mangling=False) == \
                        '      exp(x_) + sin(x*y) + cos(X*Y)'
    assert fcode(x - cos(X), name_mangling=False) == '      x - cos(X)'
    assert ob.doprint(X*sin(x) + x_, assign_to='me') == '      me = X*sin(x_) + x__'
    assert ob.doprint(X*sin(x), assign_to='mu') == '      mu = X*sin(x_)'
    assert ob.doprint(x_, assign_to='ad') == '      ad = x__'
    n, m = symbols('n,m', integer=True)
    A = IndexedBase('A')
    x = IndexedBase('x')
    y = IndexedBase('y')
    i = Idx('i', m)
    I = Idx('I', n)
    assert fcode(A[i, I]*x[I], assign_to=y[i], source_format='free') == (
                                            "do i = 1, m\n"
                                            "   y(i) = 0\n"
                                            "end do\n"
                                            "do i = 1, m\n"
                                            "   do I_ = 1, n\n"
                                            "      y(i) = A(i, I_)*x(I_) + y(i)\n"
                                            "   end do\n"
                                            "end do" )

