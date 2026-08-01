
def _endprint(x, flag, fval, maxfun, xtol, disp):
    if flag == 0:
        if disp > 1:
            print("\nOptimization terminated successfully;\n"
                  "The returned value satisfies the termination criteria\n"
                  "(using xtol = ", xtol, ")")
        return

    if flag == 1:
        msg = ("\nMaximum number of function evaluations exceeded --- "
               "increase maxfun argument.\n")
    elif flag == 2:
        msg = f"\n{_status_message['nan']}"

    _print_success_message_or_warn(flag, msg)
    return

