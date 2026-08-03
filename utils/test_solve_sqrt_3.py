import re

def test_solve_sqrt_3():
    R = Symbol('R')
    eq = sqrt(2)*R*sqrt(1/(R + 1)) + (R + 1)*(sqrt(2)*sqrt(1/(R + 1)) - 1)
    sol = solveset_complex(eq, R)
    fset = [Rational(5, 3) + 4*sqrt(10)*cos(atan(3*sqrt(111)/251)/3)/3,
            -sqrt(10)*cos(atan(3*sqrt(111)/251)/3)/3 +
            40*re(1/((Rational(-1, 2) - sqrt(3)*I/2)*(Rational(251, 27) + sqrt(111)*I/9)**Rational(1, 3)))/9 +
            sqrt(30)*sin(atan(3*sqrt(111)/251)/3)/3 + Rational(5, 3) +
            I*(-sqrt(30)*cos(atan(3*sqrt(111)/251)/3)/3 -
               sqrt(10)*sin(atan(3*sqrt(111)/251)/3)/3 +
               40*im(1/((Rational(-1, 2) - sqrt(3)*I/2)*(Rational(251, 27) + sqrt(111)*I/9)**Rational(1, 3)))/9)]
    cset = [40*re(1/((Rational(-1, 2) + sqrt(3)*I/2)*(Rational(251, 27) + sqrt(111)*I/9)**Rational(1, 3)))/9 -
            sqrt(10)*cos(atan(3*sqrt(111)/251)/3)/3 - sqrt(30)*sin(atan(3*sqrt(111)/251)/3)/3 +
            Rational(5, 3) +
            I*(40*im(1/((Rational(-1, 2) + sqrt(3)*I/2)*(Rational(251, 27) + sqrt(111)*I/9)**Rational(1, 3)))/9 -
               sqrt(10)*sin(atan(3*sqrt(111)/251)/3)/3 +
               sqrt(30)*cos(atan(3*sqrt(111)/251)/3)/3)]

    fs = FiniteSet(*fset)
    cs = ConditionSet(R, Eq(eq, 0), FiniteSet(*cset))
    assert sol == (fs - {-1}) | (cs - {-1})

    # the number of real roots will depend on the value of m: for m=1 there are 4
    # and for m=-1 there are none.
    eq = -sqrt((m - q)**2 + (-m/(2*q) + S.Half)**2) + sqrt((-m**2/2 - sqrt(
        4*m**4 - 4*m**2 + 8*m + 1)/4 - Rational(1, 4))**2 + (m**2/2 - m - sqrt(
            4*m**4 - 4*m**2 + 8*m + 1)/4 - Rational(1, 4))**2)
    unsolved_object = ConditionSet(q, Eq(sqrt((m - q)**2 + (-m/(2*q) + S.Half)**2) -
        sqrt((-m**2/2 - sqrt(4*m**4 - 4*m**2 + 8*m + 1)/4 - Rational(1, 4))**2 + (m**2/2 - m -
        sqrt(4*m**4 - 4*m**2 + 8*m + 1)/4 - Rational(1, 4))**2), 0), S.Reals)
    assert solveset_real(eq, q) == unsolved_object

