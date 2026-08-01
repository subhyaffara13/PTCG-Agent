
def test_issue_12114():
    a, b, c, d, e, f, g = symbols('a,b,c,d,e,f,g')
    terms = [1 + a*b + d*e, 1 + a*c + d*f, 1 + b*c + e*f,
             g - a**2 - d**2, g - b**2 - e**2, g - c**2 - f**2]
    sol = solve(terms, [a, b, c, d, e, f, g], dict=True)
    s = sqrt(-f**2 - 1)
    s2 = sqrt(2 - f**2)
    s3 = sqrt(6 - 3*f**2)
    s4 = sqrt(3)*f
    s5 = sqrt(3)*s2
    assert sol == [
        {a: -s, b: -s, c: -s, d: f, e: f, g: -1},
        {a: s, b: s, c: s, d: f, e: f, g: -1},
        {a: -s4/2 - s2/2, b: s4/2 - s2/2, c: s2,
            d: -f/2 + s3/2, e: -f/2 - s5/2, g: 2},
        {a: -s4/2 + s2/2, b: s4/2 + s2/2, c: -s2,
            d: -f/2 - s3/2, e: -f/2 + s5/2, g: 2},
        {a: s4/2 - s2/2, b: -s4/2 - s2/2, c: s2,
            d: -f/2 - s3/2, e: -f/2 + s5/2, g: 2},
        {a: s4/2 + s2/2, b: -s4/2 + s2/2, c: -s2,
            d: -f/2 + s3/2, e: -f/2 - s5/2, g: 2}]

