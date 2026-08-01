
def _dilogtable():
    return {
        S.Half: pi**2/12 - log(2)**2/2,
        Integer(2) : pi**2/4 - I*pi*log(2),
        -(sqrt(5) - 1)/2 : -pi**2/15 + log((sqrt(5)-1)/2)**2/2,
        -(sqrt(5) + 1)/2 : -pi**2/10 - log((sqrt(5)+1)/2)**2,
        (3 - sqrt(5))/2 : pi**2/15 - log((sqrt(5)-1)/2)**2,
        (sqrt(5) - 1)/2 : pi**2/10 - log((sqrt(5)-1)/2)**2,
        I : I*S.Catalan - pi**2/48,
        -I : -I*S.Catalan - pi**2/48,
        1 - I : pi**2/16 - I*S.Catalan - pi*I/4*log(2),
        1 + I : pi**2/16 + I*S.Catalan + pi*I/4*log(2),
        (1 - I)/2 : -log(2)**2/8 + pi*I*log(2)/8 + 5*pi**2/96 - I*S.Catalan
    }

