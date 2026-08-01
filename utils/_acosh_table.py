
def _acosh_table():
    return {
        I: log(I*(1 + sqrt(2))),
        -I: log(-I*(1 + sqrt(2))),
        S.Half: pi/3,
        Rational(-1, 2): pi*Rational(2, 3),
        sqrt(2)/2: pi/4,
        -sqrt(2)/2: pi*Rational(3, 4),
        1/sqrt(2): pi/4,
        -1/sqrt(2): pi*Rational(3, 4),
        sqrt(3)/2: pi/6,
        -sqrt(3)/2: pi*Rational(5, 6),
        (sqrt(3) - 1)/sqrt(2**3): pi*Rational(5, 12),
        -(sqrt(3) - 1)/sqrt(2**3): pi*Rational(7, 12),
        sqrt(2 + sqrt(2))/2: pi/8,
        -sqrt(2 + sqrt(2))/2: pi*Rational(7, 8),
        sqrt(2 - sqrt(2))/2: pi*Rational(3, 8),
        -sqrt(2 - sqrt(2))/2: pi*Rational(5, 8),
        (1 + sqrt(3))/(2*sqrt(2)): pi/12,
        -(1 + sqrt(3))/(2*sqrt(2)): pi*Rational(11, 12),
        (sqrt(5) + 1)/4: pi/5,
        -(sqrt(5) + 1)/4: pi*Rational(4, 5)
    }

