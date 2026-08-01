
def trrad(delta_in, dnorm, eta1, eta2, gamma1, gamma2, ratio):
    '''
    This function updates the trust region radius according to RATIO and DNORM.
    '''

    # Preconditions
    if DEBUGGING:
        assert delta_in >= dnorm > 0
        assert 0 <= eta1 <= eta2 < 1
        assert 0 < gamma1 < 1 < gamma2
        # By the definition of RATIO in ratio.f90, RATIO cannot be NaN unless the
        # actual reduction is NaN, which should NOT happen due to the moderated extreme
        # barrier.
        assert not np.isnan(ratio)

    #====================#
    # Calculation starts #
    #====================#

    if ratio <= eta1:
        delta = gamma1 * dnorm  # Powell's UOBYQA/NEWUOA
        # delta = gamma1 * delta_in  # Powell's COBYLA/LINCOA
        # delta = min(gamma1 * delta_in, dnorm)  # Powell's BOBYQA
    elif ratio <= eta2:
        delta = max(gamma1 * delta_in, dnorm)  # Powell's UOBYQA/NEWUOA/BOBYQA/LINCOA
    else:
        delta = max(gamma1 * delta_in, gamma2 * dnorm)  # Powell's NEWUOA/BOBYQA
        # delta = max(delta_in, gamma2 * dnorm)  # Modified version. Works well for UOBYQA
        # For noise-free CUTEst problems of <= 100 variables, Powell's version works slightly better
        # than the modified one.
        # delta = max(delta_in, 1.25*dnorm, dnorm + rho)  # Powell's UOBYQA
        # delta = min(max(gamma1 * delta_in, gamma2 * dnorm), gamma3 * delta_in)  # Powell's LINCOA, gamma3 = np.sqrt(2)

    # For noisy problems, the following may work better.
    # if ratio <= eta1:
    #     delta = gamma1 * dnorm
    # elseif ratio <= eta2:  # Ensure DELTA >= DELTA_IN
    #     delta = delta_in
    # else:  # Ensure DELTA > DELTA_IN with a constant factor
    #     delta = max(delta_in * (1 + gamma2) / 2, gamma2 * dnorm)

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert delta > 0
    return delta

