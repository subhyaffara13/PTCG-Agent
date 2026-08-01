
def geostep(jdrop, amat, bvec, conmat, cpen, cval, delbar, fval, simi):
    '''
    This function calculates a geometry step so that the geometry of the interpolation set is improved
    when SIM[: JDROP_GEO] is replaced with SIM[:, NUM_VARS] + D. See (15)--(17) of the COBYLA paper.
    '''

    # Sizes
    m_lcon = np.size(bvec, 0) if bvec is not None else 0
    num_constraints = np.size(conmat, 0)
    num_vars = np.size(simi, 0)

    # Preconditions
    if DEBUGGING:
        assert num_constraints >= m_lcon >= 0
        assert num_vars >= 1
        assert delbar > 0
        assert cpen > 0
        assert np.size(simi, 0) == num_vars and np.size(simi, 1) == num_vars
        assert np.isfinite(simi).all()
        assert np.size(fval) == num_vars + 1 and not any(np.isnan(fval) | np.isposinf(fval))
        assert np.size(conmat, 0) == num_constraints and np.size(conmat, 1) == num_vars + 1
        assert not np.any(np.isnan(conmat) | np.isposinf(conmat))
        assert np.size(cval) == num_vars + 1 and not any(cval < 0 | np.isnan(cval) | np.isposinf(cval))
        assert 0 <= jdrop < num_vars

    #====================#
    # Calculation starts #
    #====================#

    # SIMI[JDROP, :] is a vector perpendicular to the face of the simplex to the opposite of vertex
    # JDROP. Set D to the vector in this direction and with length DELBAR.
    d = simi[jdrop, :]
    d = delbar * (d / norm(d))

    # The code below chooses the direction of D according to an approximation of the merit function.
    # See (17) of the COBYLA paper and  line 225 of Powell's cobylb.f.

    # Calculate the coefficients of the linear approximations to the objective and constraint functions.
    # N.B.: CONMAT and SIMI have been updated after the last trust-region step, but G and A have not.
    # So we cannot pass G and A from outside.
    g = matprod(fval[:num_vars] - fval[num_vars], simi)
    A = np.zeros((num_vars, num_constraints))
    A[:, :m_lcon] = amat.T if amat is not None else amat
    A[:, m_lcon:] = matprod((conmat[m_lcon:, :num_vars] -
                          np.tile(conmat[m_lcon:, num_vars], (num_vars, 1)).T), simi).T
    # CVPD and CVND are the predicted constraint violation of D and -D by the linear models.
    cvpd = np.max(np.append(0, conmat[:, num_vars] + matprod(d, A)))
    cvnd = np.max(np.append(0, conmat[:, num_vars] - matprod(d, A)))
    if -inprod(d, g) + cpen * cvnd < inprod(d, g) + cpen * cvpd:
        d *= -1

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert np.size(d) == num_vars and all(np.isfinite(d))
        # In theory, ||S|| == DELBAR, which may be false due to rounding, but not too far.
        # It is crucial to ensure that the geometry step is nonzero, which holds in theory.
        assert 0.9 * delbar < np.linalg.norm(d) <= 1.1 * delbar
    return d

