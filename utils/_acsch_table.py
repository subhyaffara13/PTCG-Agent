
def _acsch_table():
    return {
            I: -pi / 2,
            I*(sqrt(2) + sqrt(6)): -pi / 12,
            I*(1 + sqrt(5)): -pi / 10,
            I*2 / sqrt(2 - sqrt(2)): -pi / 8,
            I*2: -pi / 6,
            I*sqrt(2 + 2/sqrt(5)): -pi / 5,
            I*sqrt(2): -pi / 4,
            I*(sqrt(5)-1): -3*pi / 10,
            I*2 / sqrt(3): -pi / 3,
            I*2 / sqrt(2 + sqrt(2)): -3*pi / 8,
            I*sqrt(2 - 2/sqrt(5)): -2*pi / 5,
            I*(sqrt(6) - sqrt(2)): -5*pi / 12,
            S(2): -I*log((1+sqrt(5))/2),
        }

