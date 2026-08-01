
def egypt_greedy(x, y):
    # assumes gcd(x, y) == 1
    if x == 1:
        return [y]
    else:
        a = (-y) % x
        b = y*(y//x + 1)
        c = gcd(a, b)
        if c > 1:
            num, denom = a//c, b//c
        else:
            num, denom = a, b
        return [y//x + 1] + egypt_greedy(num, denom)

