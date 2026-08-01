
def test_distr_params_lists():
    # distribution objects are extra distributions added in
    # test_discrete_basic. All other distributions are strings (names)
    # and so we only choose those to compare whether both lists match.
    discrete_distnames = {name for name, _ in distdiscrete
                          if isinstance(name, str)}
    invdiscrete_distnames = {name for name, _ in invdistdiscrete}
    assert discrete_distnames == invdiscrete_distnames

    cont_distnames = {name for name, _ in distcont}
    invcont_distnames = {name for name, _ in invdistcont}
    assert cont_distnames == invcont_distnames

