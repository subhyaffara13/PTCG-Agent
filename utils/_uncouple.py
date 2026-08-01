
def _uncouple(state, jn, jcoupling_list):
    if isinstance(state, CoupledSpinState):
        jn = state.jn
        coupled_n = state.coupled_n
        coupled_jn = state.coupled_jn
        evect = state.uncoupled_class()
    elif isinstance(state, SpinState):
        if jn is None:
            raise ValueError("Must specify j-values for coupled state")
        if not isinstance(jn, (list, tuple)):
            raise TypeError("jn must be list or tuple")
        if jcoupling_list is None:
            # Use default
            jcoupling_list = []
            for i in range(1, len(jn)):
                jcoupling_list.append(
                    (1, 1 + i, Add(*[jn[j] for j in range(i + 1)])) )
        if not isinstance(jcoupling_list, (list, tuple)):
            raise TypeError("jcoupling must be a list or tuple")
        if not len(jcoupling_list) == len(jn) - 1:
            raise ValueError("Must specify 2 fewer coupling terms than the number of j values")
        coupled_n, coupled_jn = _build_coupled(jcoupling_list, len(jn))
        evect = state.__class__
    else:
        raise TypeError("state must be a spin state")
    j = state.j
    m = state.m
    coupling_list = []
    j_list = list(jn)

    # Create coupling, which defines all the couplings between all the spaces
    for j3, (n1, n2) in zip(coupled_jn, coupled_n):
        # j's which are coupled as first and second spaces
        j1 = j_list[n1[0] - 1]
        j2 = j_list[n2[0] - 1]
        # Build coupling list
        coupling_list.append( (n1, n2, j1, j2, j3) )
        # Set new value in j_list
        j_list[min(n1 + n2) - 1] = j3

    if j.is_number and m.is_number:
        diff_max = [ 2*x for x in jn ]
        diff = Add(*jn) - m

        n = len(jn)
        tot = binomial(diff + n - 1, diff)

        result = []
        for config_num in range(tot):
            diff_list = _confignum_to_difflist(config_num, diff, n)
            if any(d > p for d, p in zip(diff_list, diff_max)):
                continue

            cg_terms = []
            for coupling in coupling_list:
                j1_n, j2_n, j1, j2, j3 = coupling
                m1 = Add( *[ jn[x - 1] - diff_list[x - 1] for x in j1_n ] )
                m2 = Add( *[ jn[x - 1] - diff_list[x - 1] for x in j2_n ] )
                m3 = m1 + m2
                cg_terms.append( (j1, m1, j2, m2, j3, m3) )
            coeff = Mul( *[ CG(*term).doit() for term in cg_terms ] )
            state = TensorProduct(
                *[ evect(j, j - d) for j, d in zip(jn, diff_list) ] )
            result.append(coeff*state)
        return Add(*result)
    else:
        # Symbolic coupling
        m_str = "m1:%d" % (len(jn) + 1)
        mvals = symbols(m_str)
        cg_terms = [(j1, Add(*[mvals[n - 1] for n in j1_n]),
                     j2, Add(*[mvals[n - 1] for n in j2_n]),
                     j3, Add(*[mvals[n - 1] for n in j1_n + j2_n])) for j1_n, j2_n, j1, j2, j3 in coupling_list[:-1] ]
        cg_terms.append(*[(j1, Add(*[mvals[n - 1] for n in j1_n]),
                           j2, Add(*[mvals[n - 1] for n in j2_n]),
                           j, m) for j1_n, j2_n, j1, j2, j3 in [coupling_list[-1]] ])
        cg_coeff = Mul(*[CG(*cg_term) for cg_term in cg_terms])
        sum_terms = [ (m, -j, j) for j, m in zip(jn, mvals) ]
        state = TensorProduct( *[ evect(j, m) for j, m in zip(jn, mvals) ] )
        return Sum(cg_coeff*state, *sum_terms)

