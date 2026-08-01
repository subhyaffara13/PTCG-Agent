
def retmsg(solver, info, iprint, nf, f, x, cstrv=None, constr=None):
    '''
    This function prints messages at return.
    '''
    # Local variables
    valid_exit_codes = [FTARGET_ACHIEVED, MAXFUN_REACHED, MAXTR_REACHED,
        SMALL_TR_RADIUS, TRSUBP_FAILED, NAN_INF_F, NAN_INF_X, NAN_INF_MODEL, DAMAGING_ROUNDING,
        NO_SPACE_BETWEEN_BOUNDS, ZERO_LINEAR_CONSTRAINT, CALLBACK_TERMINATE]

    # Preconditions
    if DEBUGGING:
        assert info in valid_exit_codes

    #====================#
    # Calculation starts #
    #====================#

    if abs(iprint) < 1:  # No printing (iprint == 0)
        return
    elif iprint > 0:  # Print the message to the standard out.
        fname = ''
    else:  # Print the message to a file named FNAME.
        fname = f'{solver}_output.txt'

    # Decide whether the problem is truly constrained.
    if present(constr):
        is_constrained = (np.size(constr) > 0)
    else:
        is_constrained = present(cstrv)

    # Decide the constraint violation.
    if present(cstrv):
        cstrv_loc = cstrv
    elif present(constr):
        cstrv_loc = np.max(np.append(0, -constr))  # N.B.: We assume that the constraint is CONSTR >= 0.
    else:
        cstrv_loc = 0

    # Decide the return message.
    ret_message = get_info_string(solver, info)

    if np.size(x) <= 2:
        x_message = f'\nThe corresponding X is: {x}'  # Printed in one line
    else:
        x_message = f'\nThe corresponding X is:\n{x}'

    if is_constrained:
        nf_message = (f'\nNumber of function values = {nf}{spaces}'
            f'Least value of F = {f}{spaces}Constraint violation = {cstrv_loc}')
    else:
        nf_message = f'\nNumber of function values = {nf}{spaces}Least value of F = {f}'

    if is_constrained and present(constr):
        if np.size(constr) <= 2:
            constr_message = f'\nThe constraint value is: {constr}'  # Printed in one line
        else:
            constr_message = f'\nThe constraint value is:\n{constr}'
    else:
        constr_message = ''

    # Print the message.
    if abs(iprint) >= 2:
        message = f'\n{ret_message}{nf_message}{x_message}{constr_message}\n'
    else:
        message = f'{ret_message}{nf_message}{x_message}{constr_message}\n'
    if len(fname) > 0:
        with open(fname, 'a') as f: f.write(message)
    else:
        print(message)

