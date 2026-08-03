import re
import sys

def mpc_hash(z):
    if sys.version_info >= (3, 2):
        re, im = z
        h = mpf_hash(re) + sys.hash_info.imag * mpf_hash(im)
        # Need to reduce either module 2^32 or 2^64
        h = h % (2**sys.hash_info.width)
        return int(h)
    else:
        try:
            return hash(mpc_to_complex(z, strict=True))
        except OverflowError:
            return hash(z)

