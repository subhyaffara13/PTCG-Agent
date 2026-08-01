
def trstlp_sub(iact: npt.NDArray, nact: int, stage, A, b, delta, d, vmultc, z):
    '''
    This subroutine does the real calculations for trstlp, both stage 1 and stage 2.
    Major differences between stage 1 and stage 2:
    1. Initialization. Stage 2 inherits the values of some variables from stage 1, so they are
    initialized in stage 1 but not in stage 2.
    2. cviol. cviol is updated after at iteration in stage 1, while it remains a constant in stage2.
    3. sdirn. See the definition of sdirn in the code for details.
    4. optnew. The two stages have different objectives, so optnew is updated differently.
    5. step. step <= cviol in stage 1.
    '''
    zdasav = np.zeros(z.shape[1])
    vmultd = np.zeros(np.size(vmultc))
    zdota = np.zeros(np.size(z, 1))

    # Sizes
    mcon = np.size(A, 1)
    num_vars = np.size(A, 0)

    # Preconditions
    if DEBUGGING:
        assert num_vars >= 1
        assert stage == 1 or stage == 2
        assert (mcon >= 0 and stage == 1) or (mcon >= 1 and stage == 2)
        assert np.size(b) == mcon
        assert np.size(iact) == mcon
        assert np.size(vmultc) == mcon
        assert np.size(d) == num_vars
        assert np.size(z, 0) == num_vars and np.size(z, 1) == num_vars
        assert delta > 0
        if stage == 2:
            assert all(np.isfinite(d)) and np.linalg.norm(d) <= 2 * delta
            assert nact >= 0 and nact <= np.minimum(mcon, num_vars)
            assert all(vmultc[:mcon]) >= 0
            # N.B.: Stage 1 defines only VMULTC(1:M); VMULTC(M+1) is undefined!


    # Initialize according to stage
    if stage == 1:
        iact = np.linspace(0, mcon-1, mcon, dtype=int)
        nact = 0
        d = np.zeros(num_vars)
        cviol = np.max(np.append(0, -b))
        vmultc = cviol + b
        z = np.eye(num_vars)
        if mcon == 0 or cviol <= 0:
            # Check whether a quick return is possible. Make sure the in-outputs have been initialized.
            return iact, nact, d, vmultc, z

        if all(np.isnan(b)):
            return iact, nact, d, vmultc, z
        else:
            icon = np.nanargmax(-b)
        num_constraints = mcon
        sdirn = np.zeros(len(d))
    else:
        if inprod(d, d) >= delta*delta:
            # Check whether a quick return is possible.
            return iact, nact, d, vmultc, z

        iact[mcon-1] = mcon-1
        vmultc[mcon-1] = 0
        num_constraints = mcon - 1
        icon = mcon - 1

        # In Powell's code, stage 2 uses the zdota and cviol calculated by stage1. Here we recalculate
        # them so that they need not be passed from stage 1 to 2, and hence the coupling is reduced.
        cviol = np.max(np.append(0, matprod(d, A[:, :num_constraints]) - b[:num_constraints]))
    zdota[:nact] = [inprod(z[:, k], A[:, iact[k]]) for k in range(nact)]

    # More initialization
    optold = REALMAX
    nactold = nact
    nfail = 0

    # Zaikun 20211011: vmultd is computed from scratch at each iteration, but vmultc is inherited

    # Powell's code can encounter infinite cycling, which did happen when testing the following CUTEst
    # problems: DANWOODLS, GAUSS1LS, GAUSS2LS, GAUSS3LS, KOEBHELB, TAX13322, TAXR13322. Indeed, in all
    # these cases, Inf/NaN appear in d due to extremely large values in A (up to 10^219). To resolve
    # this, we set the maximal number of iterations to maxiter, and terminate if Inf/NaN occurs in d.
    maxiter = np.minimum(10000, 100*max(num_constraints, num_vars))
    for iter in range(maxiter):
        if DEBUGGING:
            assert all(vmultc >= 0)
        if stage == 1:
            optnew = cviol
        else:
            optnew = inprod(d, A[:, mcon-1])

        # End the current stage of the calculation if 3 consecutive iterations have either failed to
        # reduce the best calculated value of the objective function or to increase the number of active
        # constraints since the best value was calculated. This strategy prevents cycling, but there is
        # a remote possibility that it will cause premature termination.
        if optnew < optold or nact > nactold:
            nactold = nact
            nfail = 0
        else:
            nfail += 1
        optold = np.minimum(optold, optnew)
        if nfail == 3:
            break

        # If icon exceeds nact, then we add the constraint with index iact[icon] to the active set.
        if icon >= nact:  # In Python this needs to be >= since Python is 0-indexed (in Fortran we have 1 > 0, in Python we need 0 >= 0)
            zdasav[:nact] = zdota[:nact]
            nactsav = nact
            z, zdota, nact = qradd_Rdiag(A[:, iact[icon]], z, zdota, nact)  # May update nact to nact+1
            # Indeed it suffices to pass zdota[:min(num_vars, nact+1)] to qradd as follows:
            # qradd(A[:, iact[icon]], z, zdota[:min(num_vars, nact+1)], nact)

            if nact == nactsav + 1:
                # N.B.: It is possible to index arrays using [nact, icon] when nact == icon.
                # Zaikun 20211012: Why should vmultc[nact] = 0?
                if nact != (icon + 1):  # Need to add 1 to Python for 0 indexing
                    vmultc[[icon, nact-1]] = vmultc[nact-1], 0
                    iact[[icon, nact-1]] = iact[[nact-1, icon]]
                else:
                    vmultc[nact-1] = 0
            else:
                # Zaikun 20211011:
                # 1. VMULTD is calculated from scratch for the first time (out of 2) in one iteration.
                # 2. Note that IACT has not been updated to replace IACT[NACT] with IACT[ICON]. Thus
                # A[:, IACT[:NACT]] is the UNUPDATED version before QRADD (note Z[:, :NACT] remains the
                # same before and after QRADD). Therefore if we supply ZDOTA to LSQR (as Rdiag) as
                # Powell did, we should use the UNUPDATED version, namely ZDASAV.
                # vmultd[:nact] = lsqr(A[:, iact[:nact]], A[:, iact[icon]], z[:, :nact], zdasav[:nact])
                vmultd[:nact] = lsqr(A[:, iact[:nact]], A[:, iact[icon]], z[:, :nact], zdasav[:nact])
                if not any(np.logical_and(vmultd[:nact] > 0, iact[:nact] <= num_constraints)):
                    # N.B.: This can be triggered by NACT == 0 (among other possibilities)! This is
                    # important, because NACT will be used as an index in the sequel.
                    break
                # vmultd[NACT+1:mcon] is not used, but we have to initialize it in Fortran, or compilers
                # complain about the where construct below (another solution: restrict where to 1:NACT).
                vmultd[nact:mcon] = -1  # len(vmultd) == mcon

                # Revise the Lagrange multipliers. The revision is not applicable to vmultc[nact:num_constraints].
                fracmult = [vmultc[i]/vmultd[i] if vmultd[i] > 0 and iact[i] <= num_constraints else REALMAX for i in range(nact)]
                # Only the places with vmultd > 0 and iact <= m is relevant below, if any.
                frac = min(fracmult[:nact])  # fracmult[nact:mcon] may contain garbage
                vmultc[:nact] = np.maximum(np.zeros(len(vmultc[:nact])), vmultc[:nact] - frac*vmultd[:nact])

                # Reorder the active constraints so that the one to be replaced is at the end of the list.
                # Exit if the new value of zdota[nact] is not acceptable. Powell's condition for the
                # following If: not abs(zdota[nact]) > 0. Note that it is different from
                # 'abs(zdota[nact]) <=0)' as zdota[nact] can be NaN.
                # N.B.: We cannot arrive here with nact == 0, which should have triggered a break above
                if np.isnan(zdota[nact - 1]) or abs(zdota[nact - 1]) <= EPS**2:
                    break
                vmultc[[icon, nact - 1]] = 0, frac  # vmultc[[icon, nact]] is valid as icon > nact
                iact[[icon, nact - 1]] = iact[[nact - 1, icon]]
            # end if nact == nactsav + 1

            # In stage 2, ensure that the objective continues to be treated as the last active constraint.
            # Zaikun 20211011, 20211111: Is it guaranteed for stage 2 that iact[nact-1] = mcon when
            # iact[nact] != mcon??? If not, then how does the following procedure ensure that mcon is
            # the last of iact[:nact]?
            if stage == 2 and iact[nact - 1] != (mcon - 1):
                if nact <= 1:
                    # We must exit, as nact-2 is used as an index below. Powell's code does not have this.
                    break
                z, zdota[:nact] = qrexc_Rdiag(A[:, iact[:nact]], z, zdota[:nact], nact - 2)  # We pass nact-2 in Python instead of nact-1
                # Indeed, it suffices to pass Z[:, :nact] to qrexc as follows:
                # z[:, :nact], zdota[:nact] = qrexc(A[:, iact[:nact]], z[:, :nact], zdota[:nact], nact - 1)
                iact[[nact-2, nact-1]] = iact[[nact-1, nact-2]]
                vmultc[[nact-2, nact-1]] = vmultc[[nact-1, nact-2]]
            # Zaikun 20211117: It turns out that the last few lines do not guarantee iact[nact] == num_vars in
            # stage 2; the following test cannot be passed. IS THIS A BUG?!
            # assert iact[nact] == mcon or stage == 1, 'iact[nact] must == mcon in stage 2'

            # Powell's code does not have the following. It avoids subsequent floating points exceptions.
            if np.isnan(zdota[nact-1]) or abs(zdota[nact-1]) <= EPS**2:
                break

            # Set sdirn to the direction of the next change to the current vector of variables
            # Usually during stage 1 the vector sdirn gives a search direction that reduces all the
            # active constraint violations by one simultaneously.
            if stage == 1:
                sdirn -= ((inprod(sdirn, A[:, iact[nact-1]]) + 1)/zdota[nact-1])*z[:, nact-1]
            else:
                sdirn = -1/zdota[nact-1]*z[:, nact-1]
        else:  # icon < nact
            # Delete the constraint with the index iact[icon] from the active set, which is done by
            # reordering iact[icon:nact] into [iact[icon+1:nact], iact[icon]] and then reduce nact to
            # nact - 1. In theory, icon > 0.
            # assert icon > 0, "icon > 0 is required"  #  For Python I think this is irrelevant
            z, zdota[:nact] = qrexc_Rdiag(A[:, iact[:nact]], z, zdota[:nact], icon)  # qrexc does nothing if icon == nact
            # Indeed, it suffices to pass Z[:, :nact] to qrexc as follows:
            # z[:, :nact], zdota[:nact] = qrexc(A[:, iact[:nact]], z[:, :nact], zdota[:nact], icon)
            iact[icon:nact] = [*iact[icon+1:nact], iact[icon]]
            vmultc[icon:nact] = [*vmultc[icon+1:nact], vmultc[icon]]
            nact -= 1

            # Powell's code does not have the following. It avoids subsequent exceptions.
            # Zaikun 20221212: In theory, nact > 0 in stage 2, as the objective function should always
            # be considered as an "active constraint" --- more precisely, iact[nact] = mcon. However,
            # looking at the code, I cannot see why in stage 2 nact must be positive after the reduction
            # above. It did happen in stage 1 that nact became 0 after the reduction --- this is
            # extremely rare, and it was never observed until 20221212, after almost one year of
            # random tests. Maybe nact is theoretically positive even in stage 1?
            if stage == 2 and nact < 0:
                break  # If this case ever occurs, we have to break, as nact is used as an index below.
            if nact > 0:
                if np.isnan(zdota[nact-1]) or abs(zdota[nact-1]) <= EPS**2:
                    break

            # Set sdirn to the direction of the next change to the current vector of variables.
            if stage == 1:
                sdirn -= inprod(sdirn, z[:, nact]) * z[:, nact]
                # sdirn is orthogonal to z[:, nact+1]
            else:
                sdirn = -1/zdota[nact-1] * z[:, nact-1]
        # end if icon > nact

        # Calculate the step to the trust region boundary or take the step that reduces cviol to 0.
        # ----------------------------------------------------------------------------------------- #
        # The following calculation of step is adopted from NEWUOA/BOBYQA/LINCOA. It seems to improve
        # the performance of COBYLA. We also found that removing the precaution about underflows is
        # beneficial to the overall performance of COBYLA --- the underflows are harmless anyway.
        dd = delta*delta - inprod(d, d)
        ss = inprod(sdirn, sdirn)
        sd = inprod(sdirn, d)
        if dd <= 0 or ss <= EPS * delta*delta or np.isnan(sd):
            break
        # sqrtd: square root of a discriminant. The max avoids sqrtd < abs(sd) due to underflow
        sqrtd = max(np.sqrt(ss*dd + sd*sd), abs(sd), np.sqrt(ss * dd))
        if sd > 0:
            step = dd / (sqrtd + sd)
        else:
            step = (sqrtd - sd) / ss
        # step < 0 should not happen. Step can be 0 or NaN when, e.g., sd or ss becomes inf
        if step <= 0 or not np.isfinite(step):
            break

        # Powell's approach and comments are as follows.
        # -------------------------------------------------- #
        # The two statements below that include the factor eps prevent
        # some harmless underflows that occurred in a test calculation
        # (Zaikun: here, eps is the machine epsilon; Powell's original
        # code used 1.0e-6, and Powell's code was written in single
        # precision). Further, we skip the step if it could be 0 within
        # a reasonable tolerance for computer rounding errors.

        #  !dd = delta*delta - sum(d**2, mask=(abs(d) >= EPS * delta))
        #  !ss = inprod(sdirn, sdirn)
        #  !if (dd  <= 0) then
        #  !    exit
        #  !end if
        #  !sd = inprod(sdirn, d)
        #  !if (abs(sd) >= EPS * sqrt(ss * dd)) then
        #  !    step = dd / (sqrt(ss * dd + sd*sd) + sd)
        #  !else
        #  !    step = dd / (sqrt(ss * dd) + sd)
        #  !end if
        # -------------------------------------------------- #

        if stage == 1:
            if isminor(cviol, step):
                break
            step = min(step, cviol)

        # Set dnew to the new variables if step is the steplength, and reduce cviol to the corresponding
        # maximum residual if stage 1 is being done
        dnew = d + step * sdirn
        if stage == 1:
            cviol = np.max(np.append(0, matprod(dnew, A[:, iact[:nact]]) - b[iact[:nact]]))
            # N.B.: cviol will be used when calculating vmultd[nact+1:mcon].

        # Zaikun 20211011:
        # 1. vmultd is computed from scratch for the second (out of 2) time in one iteration.
        # 2. vmultd[:nact] and vmultd[nact:mcon] are calculated separately with no coupling.
        # 3. vmultd will be calculated from scratch again in the next iteration.
        # Set vmultd to the vmultc vector that would occur if d became dnew. A device is included to
        # force vmultd[k] = 0 if deviations from this value can be attributed to computer rounding
        # errors. First calculate the new Lagrange multipliers.
        vmultd[:nact] = -lsqr(A[:, iact[:nact]], dnew, z[:, :nact], zdota[:nact])
        if stage == 2:
            vmultd[nact-1] = max(0, vmultd[nact-1])  # This seems never activated.
        # Complete vmultd by finding the new constraint residuals. (Powell wrote "Complete vmultc ...")
        cvshift = cviol - (matprod(dnew, A[:, iact]) - b[iact])  # Only cvshift[nact+1:mcon] is needed
        cvsabs = matprod(abs(dnew), abs(A[:, iact])) + abs(b[iact]) + cviol
        cvshift[isminor(cvshift, cvsabs)] = 0
        vmultd[nact:mcon] = cvshift[nact:mcon]

        # Calculate the fraction of the step from d to dnew that will be taken
        fracmult = [vmultc[i]/(vmultc[i] - vmultd[i]) if vmultd[i] < 0 else REALMAX for i in range(len(vmultd))]
        # Only the places with vmultd < 0 are relevant below, if any.
        icon = np.argmin(np.append(1, fracmult)) - 1
        frac = min(np.append(1, fracmult))

        # Update d, vmultc, and cviol
        dold = d
        d = (1 - frac)*d + frac * dnew
        vmultc = np.maximum(0, (1 - frac)*vmultc + frac*vmultd)
        # Break in the case of inf/nan in d or vmultc.
        if not (np.isfinite(primasum(abs(d))) and np.isfinite(primasum(abs(vmultc)))):
            d = dold  # Should we restore also iact, nact, vmultc, and z?
            break

        if stage == 1:
            # cviol = (1 - frac) * cvold + frac * cviol  # Powell's version
            # In theory, cviol = np.max(np.append(d@A - b, 0)), yet the
            # cviol updated as above can be quite different from this value if A has huge entries (e.g., > 1e20)
            cviol = np.max(np.append(0, matprod(d, A) - b))

        if icon < 0 or icon >= mcon:
            # In Powell's code, the condition is icon == 0. Indeed, icon < 0 cannot hold unless
            # fracmult contains only nan, which should not happen; icon >= mcon should never occur.
            break

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert np.size(iact) == mcon
        assert np.size(vmultc) == mcon
        assert all(vmultc >= 0)
        assert np.size(d) == num_vars
        assert all(np.isfinite(d))
        assert np.linalg.norm(d) <= 2 * delta
        assert np.size(z, 0) == num_vars and np.size(z, 1) == num_vars
        assert nact >= 0 and nact <= np.minimum(mcon, num_vars)

    return iact, nact, d, vmultc, z

