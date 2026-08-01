
def rhomsg(solver, iprint, nf, delta, f, rho, x, cstrv=None, constr=None, cpen=None):
    '''
    This function prints messages when RHO is updated.
    '''

    #====================#
    # Calculation starts #
    #====================#

    if abs(iprint) < 2:  # No printing
        return
    elif iprint > 0:  # Print the message to the standard out.
        fname = ''
    else:  # Print the message to a file named FNAME.
        fname = f'{solver.strip()}_output.txt'

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

    if present(cpen):
        rho_message = (f'\nNew RHO = {rho}{spaces}Delta = {delta}{spaces}'
            f'CPEN = {cpen}')
    else:
        rho_message = f'\nNew RHO = {rho}{spaces}Delta = {delta}'

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
    if abs(iprint) >= 3:
        message = f'\n{rho_message}{nf_message}{x_message}{constr_message}'
    else:
        message = f'{rho_message}{nf_message}{x_message}{constr_message}'
    if len(fname) > 0:
        with open(fname, 'a') as f: f.write(message)
    else:
        print(message)

