
def cotpi(x):
    try:
        return cospi(x) / sinpi(x)
    except OverflowError:
        if complex(x).imag > 10:
            return -1j
        if complex(x).imag < 10:
            return 1j
        raise

