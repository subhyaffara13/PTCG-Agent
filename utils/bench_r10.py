
def bench_R10():
    "v = [-pi,-pi+1/10..,pi]"
    def srange(min, max, step):
        v = [min]
        while (max - v[-1]).evalf() > 0:
            v.append(v[-1] + step)
        return v[:-1]
    srange(-pi, pi, sympify(1)/10)

