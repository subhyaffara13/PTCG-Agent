
def test_multi_exp():
    k1, k2, k3 = symbols('k1, k2, k3')
    assert dumeq(solveset(exp(exp(x)) - 5, x),\
         imageset(Lambda(((k1, n),), I*(2*k1*pi + arg(2*n*I*pi + log(5))) + log(Abs(2*n*I*pi + log(5)))),\
             ProductSet(S.Integers, S.Integers)))
    assert dumeq(solveset((d*exp(exp(a*x + b)) + c), x),\
        imageset(Lambda(x, (-b + x)/a), ImageSet(Lambda(((k1, n),), \
            I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))) + log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d))))), \
                ProductSet(S.Integers, S.Integers))))

    assert dumeq(solveset((d*exp(exp(exp(a*x + b))) + c), x),\
        imageset(Lambda(x, (-b + x)/a), ImageSet(Lambda(((k2, k1, n),), \
            I*(2*k2*pi + arg(I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))) + \
                log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))))) + log(Abs(I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + \
                    log(Abs(c/d)))) + log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d))))))), \
                        ProductSet(S.Integers, S.Integers, S.Integers))))

    assert dumeq(solveset((d*exp(exp(exp(exp(a*x + b)))) + c), x),\
        ImageSet(Lambda(x, (-b + x)/a), ImageSet(Lambda(((k3, k2, k1, n),), \
            I*(2*k3*pi + arg(I*(2*k2*pi + arg(I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))) + \
                log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))))) + log(Abs(I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + \
                    log(Abs(c/d)))) + log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))))))) + log(Abs(I*(2*k2*pi + \
                        arg(I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))) + log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))))) + \
                            log(Abs(I*(2*k1*pi + arg(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d)))) + log(Abs(I*(2*n*pi + arg(-c/d)) + log(Abs(c/d))))))))), \
             ProductSet(S.Integers, S.Integers, S.Integers, S.Integers))))

