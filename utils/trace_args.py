import sys

def trace_args(func):
    def tofloat(x):
        if isinstance(x, mpmath.mpc):
            return complex(x)
        else:
            return float(x)

    def wrap(*a, **kw):
        sys.stderr.write(f"{tuple(map(tofloat, a))!r}: ")
        sys.stderr.flush()
        try:
            r = func(*a, **kw)
            sys.stderr.write(f"-> {r!r}")
        finally:
            sys.stderr.write("\n")
            sys.stderr.flush()
        return r
    return wrap

