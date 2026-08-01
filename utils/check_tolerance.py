
def check_tolerance(ftol, xtol, gtol, method):
    def check(tol, name):
        if tol is None:
            tol = 0
        elif tol < EPS:
            warn(f"Setting `{name}` below the machine epsilon ({EPS:.2e}) effectively "
                 f"disables the corresponding termination condition.",
                 stacklevel=3)
        return tol

    ftol = check(ftol, "ftol")
    xtol = check(xtol, "xtol")
    gtol = check(gtol, "gtol")

    if method == "lm" and (ftol < EPS or xtol < EPS or gtol < EPS):
        raise ValueError("All tolerances must be higher than machine epsilon "
                         f"({EPS:.2e}) for method 'lm'.")
    elif ftol < EPS and xtol < EPS and gtol < EPS:
        raise ValueError("At least one of the tolerances must be higher than "
                         f"machine epsilon ({EPS:.2e}).")

    return ftol, xtol, gtol

