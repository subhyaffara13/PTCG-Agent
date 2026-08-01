
def bench_R8():
    "right(x^2,0,5,10^4)"
    def right(f, a, b, n):
        a = sympify(a)
        b = sympify(b)
        n = sympify(n)
        x = f.atoms(Symbol).pop()
        Deltax = (b - a)/n
        c = a
        est = 0
        for i in range(n):
            c += Deltax
            est += f.subs(x, c)
        return est*Deltax

    right(x**2, 0, 5, 10**4)

