import re

def mpc_to_complex(z, strict=False, rnd=round_fast):
    re, im = z
    return complex(to_float(re, strict, rnd), to_float(im, strict, rnd))

