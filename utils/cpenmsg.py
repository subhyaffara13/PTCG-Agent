
def cpenmsg(solver, iprint, cpen):
    '''
    This function prints a message when CPEN is updated.
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

    # Print the message.
    if abs(iprint) >= 3:
        message = f'\nSet CPEN to {cpen}'
    else:
        message = f'\n\nSet CPEN to {cpen}'
    if len(fname) > 0:
        with open(fname, 'a') as f: f.write(message)
    else:
        print(message)

