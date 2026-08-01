
def bench_R1():
    "real(f(f(f(f(f(f(f(f(f(f(i/2)))))))))))"
    def f(z):
        return sqrt(Integer(1)/3)*z**2 + I/3
    f(f(f(f(f(f(f(f(f(f(I/2)))))))))).as_real_imag()[0]

