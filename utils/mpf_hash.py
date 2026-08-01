
def mpf_hash(s):
    # Duplicate the new hash algorithm introduces in Python 3.2.
    if sys.version_info >= (3, 2):
        ssign, sman, sexp, sbc = s

        # Handle special numbers
        if not sman:
            if s == fnan: return sys.hash_info.nan
            if s == finf: return sys.hash_info.inf
            if s == fninf: return -sys.hash_info.inf
        h = sman % HASH_MODULUS
        if sexp >= 0:
            sexp = sexp % HASH_BITS
        else:
            sexp = HASH_BITS - 1 - ((-1 - sexp) % HASH_BITS)
        h = (h << sexp) % HASH_MODULUS
        if ssign: h = -h
        if h == -1: h = -2
        return int(h)
    else:
        try:
            # Try to be compatible with hash values for floats and ints
            return hash(to_float(s, strict=1))
        except OverflowError:
            # We must unfortunately sacrifice compatibility with ints here.
            # We could do hash(man << exp) when the exponent is positive, but
            # this would cause unreasonable inefficiency for large numbers.
            return hash(s)

