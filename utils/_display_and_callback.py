
def _display_and_callback(phase_one_n, x, postsolve_args, status,
                          iteration, disp, callback):
    if phase_one_n is not None:
        phase = 1
        x_postsolve = x[:phase_one_n]
    else:
        phase = 2
        x_postsolve = x
    x_o, fun, slack, con = _postsolve(x_postsolve,
                                      postsolve_args)

    if callback is not None:
        res = OptimizeResult({'x': x_o, 'fun': fun, 'slack': slack,
                              'con': con, 'nit': iteration,
                              'phase': phase, 'complete': False,
                              'status': status, 'message': "",
                              'success': False})
        callback(res)
    if disp:
        _display_iter(phase, iteration, slack, con, fun)

