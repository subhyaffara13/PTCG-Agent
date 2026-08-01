
def get_integer_part(expr: Expr, no: int, options: OPT_DICT, return_ints=False) -> \
        TMP_RES | tuple[int, int]:
    """
    With no = 1, computes ceiling(expr)
    With no = -1, computes floor(expr)

    Note: this function either gives the exact result or signals failure.
    """
    from sympy.functions.elementary.complexes import re, im
    # The expression is likely less than 2^30 or so
    assumed_size = 30
    result = evalf(expr, assumed_size, options)
    if result is S.ComplexInfinity:
        raise ValueError("Cannot get integer part of Complex Infinity")
    ire, iim, ire_acc, iim_acc = result

    # We now know the size, so we can calculate how much extra precision
    # (if any) is needed to get within the nearest integer
    if ire and iim:
        gap = max(fastlog(ire) - ire_acc, fastlog(iim) - iim_acc)
    elif ire:
        gap = fastlog(ire) - ire_acc
    elif iim:
        gap = fastlog(iim) - iim_acc
    else:
        # ... or maybe the expression was exactly zero
        if return_ints:
            return 0, 0
        else:
            return None, None, None, None

    margin = 10

    if gap >= -margin:
        prec = margin + assumed_size + gap
        ire, iim, ire_acc, iim_acc = evalf(
            expr, prec, options)
    else:
        prec = assumed_size

    # We can now easily find the nearest integer, but to find floor/ceil, we
    # must also calculate whether the difference to the nearest integer is
    # positive or negative (which may fail if very close).
    def calc_part(re_im: Expr, nexpr: MPF_TUP):
        from .add import Add
        _, _, exponent, _ = nexpr
        is_int = exponent == 0
        nint = int(to_int(nexpr, rnd))
        if is_int:
            # make sure that we had enough precision to distinguish
            # between nint and the re or im part (re_im) of expr that
            # was passed to calc_part
            ire, iim, ire_acc, iim_acc = evalf(
                re_im - nint, 10, options)  # don't need much precision
            assert not iim
            size = -fastlog(ire) + 2  # -ve b/c ire is less than 1
            if size > prec:
                ire, iim, ire_acc, iim_acc = evalf(
                    re_im, size, options)
                assert not iim
                nexpr = ire
            nint = int(to_int(nexpr, rnd))
            _, _, new_exp, _ = ire
            is_int = new_exp == 0
        if not is_int:
            # if there are subs and they all contain integer re/im parts
            # then we can (hopefully) safely substitute them into the
            # expression
            s = options.get('subs', False)
            if s:
                # use strict=False with as_int because we take
                # 2.0 == 2
                def is_int_reim(x):
                    """Check for integer or integer + I*integer."""
                    try:
                        as_int(x, strict=False)
                        return True
                    except ValueError:
                        try:
                            [as_int(i, strict=False) for i in x.as_real_imag()]
                            return True
                        except ValueError:
                            return False

                if all(is_int_reim(v) for v in s.values()):
                    re_im = re_im.subs(s)

            re_im = Add(re_im, -nint, evaluate=False)
            x, _, x_acc, _ = evalf(re_im, 10, options)
            try:
                check_target(re_im, (x, None, x_acc, None), 3)
            except PrecisionExhausted:
                if not re_im.equals(0):
                    raise PrecisionExhausted
                x = fzero
            nint += int(no*(mpf_cmp(x or fzero, fzero) == no))
        nint = from_int(nint)
        return nint, INF

    re_, im_, re_acc, im_acc = None, None, None, None

    if ire is not None and ire != fzero:
        re_, re_acc = calc_part(re(expr, evaluate=False), ire)
    if iim is not None and iim != fzero:
        im_, im_acc = calc_part(im(expr, evaluate=False), iim)

    if return_ints:
        return int(to_int(re_ or fzero)), int(to_int(im_ or fzero))
    return re_, im_, re_acc, im_acc

