
def _couple(tp, jcoupling_list):
    states = tp.args
    coupled_evect = states[0].coupled_class()

    # Define default coupling if none is specified
    if jcoupling_list is None:
        jcoupling_list = []
        for n in range(1, len(states)):
            jcoupling_list.append( (1, n + 1) )

    # Check jcoupling_list valid
    if not len(jcoupling_list) == len(states) - 1:
        raise TypeError('jcoupling_list must be length %d, got %d' %
                        (len(states) - 1, len(jcoupling_list)))
    if not all( len(coupling) == 2 for coupling in jcoupling_list):
        raise ValueError('Each coupling must define 2 spaces')
    if any(n1 == n2 for n1, n2 in jcoupling_list):
        raise ValueError('Spin spaces cannot couple to themselves')
    if all(sympify(n1).is_number and sympify(n2).is_number for n1, n2 in jcoupling_list):
        j_test = [0]*len(states)
        for n1, n2 in jcoupling_list:
            if j_test[n1 - 1] == -1 or j_test[n2 - 1] == -1:
                raise ValueError('Spaces coupling j_n\'s are referenced by smallest n value')
            j_test[max(n1, n2) - 1] = -1

    # j values of states to be coupled together
    jn = [state.j for state in states]
    mn = [state.m for state in states]

    # Create coupling_list, which defines all the couplings between all
    # the spaces from jcoupling_list
    coupling_list = []
    n_list = [ [i + 1] for i in range(len(states)) ]
    for j_coupling in jcoupling_list:
        # Least n for all j_n which is coupled as first and second spaces
        n1, n2 = j_coupling
        # List of all n's coupled in first and second spaces
        j1_n = list(n_list[n1 - 1])
        j2_n = list(n_list[n2 - 1])
        coupling_list.append( (j1_n, j2_n) )
        # Set new j_n to be coupling of all j_n in both first and second spaces
        n_list[ min(n1, n2) - 1 ] = sorted(j1_n + j2_n)

    if all(state.j.is_number and state.m.is_number for state in states):
        # Numerical coupling
        # Iterate over difference between maximum possible j value of each coupling and the actual value
        diff_max = [ Add( *[ jn[n - 1] - mn[n - 1] for n in coupling[0] +
                         coupling[1] ] ) for coupling in coupling_list ]
        result = []
        for diff in range(diff_max[-1] + 1):
            # Determine available configurations
            n = len(coupling_list)
            tot = binomial(diff + n - 1, diff)

            for config_num in range(tot):
                diff_list = _confignum_to_difflist(config_num, diff, n)

                # Skip the configuration if non-physical
                # This is a lazy check for physical states given the loose restrictions of diff_max
                if any(d > m for d, m in zip(diff_list, diff_max)):
                    continue

                # Determine term
                cg_terms = []
                coupled_j = list(jn)
                jcoupling = []
                for (j1_n, j2_n), coupling_diff in zip(coupling_list, diff_list):
                    j1 = coupled_j[ min(j1_n) - 1 ]
                    j2 = coupled_j[ min(j2_n) - 1 ]
                    j3 = j1 + j2 - coupling_diff
                    coupled_j[ min(j1_n + j2_n) - 1 ] = j3
                    m1 = Add( *[ mn[x - 1] for x in j1_n] )
                    m2 = Add( *[ mn[x - 1] for x in j2_n] )
                    m3 = m1 + m2
                    cg_terms.append( (j1, m1, j2, m2, j3, m3) )
                    jcoupling.append( (min(j1_n), min(j2_n), j3) )
                # Better checks that state is physical
                if any(abs(term[5]) > term[4] for term in cg_terms):
                    continue
                if any(term[0] + term[2] < term[4] for term in cg_terms):
                    continue
                if any(abs(term[0] - term[2]) > term[4] for term in cg_terms):
                    continue
                coeff = Mul( *[ CG(*term).doit() for term in cg_terms] )
                state = coupled_evect(j3, m3, jn, jcoupling)
                result.append(coeff*state)
        return Add(*result)
    else:
        # Symbolic coupling
        cg_terms = []
        jcoupling = []
        sum_terms = []
        coupled_j = list(jn)
        for j1_n, j2_n in coupling_list:
            j1 = coupled_j[ min(j1_n) - 1 ]
            j2 = coupled_j[ min(j2_n) - 1 ]
            if len(j1_n + j2_n) == len(states):
                j3 = symbols('j')
            else:
                j3_name = 'j' + ''.join(["%s" % n for n in j1_n + j2_n])
                j3 = symbols(j3_name)
            coupled_j[ min(j1_n + j2_n) - 1 ] = j3
            m1 = Add( *[ mn[x - 1] for x in j1_n] )
            m2 = Add( *[ mn[x - 1] for x in j2_n] )
            m3 = m1 + m2
            cg_terms.append( (j1, m1, j2, m2, j3, m3) )
            jcoupling.append( (min(j1_n), min(j2_n), j3) )
            sum_terms.append((j3, m3, j1 + j2))
        coeff = Mul( *[ CG(*term) for term in cg_terms] )
        state = coupled_evect(j3, m3, jn, jcoupling)
        return Sum(coeff*state, *sum_terms)

